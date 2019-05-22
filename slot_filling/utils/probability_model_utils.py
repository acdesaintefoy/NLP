import re
import pandas as pd, numpy as np

def clean_word(word):
	word = word.replace(' ','')
	word = word.replace('.','')
	return(word)

def rm_mltp(text):
	text = re.sub(' +', ' ',text)
	return(text)

def alternative_data_base(data):
	new_data = []
	for element in data:
		for key,value in element.items():
			list_temp = []
			for dico in value:
				text = rm_mltp(dico['text'])
				for word in text.split(' '):
					if word == ' ':
						print(text)
					cleaned_word = clean_word(word)
					if cleaned_word != '':
						unite_dico = {'text' : cleaned_word}
						if 'entity' in dico.keys():
							unite_dico['entity'] = dico['entity']
						else :
							unite_dico['entity'] = 'None'
						list_temp.append(unite_dico)
		new_data.append(list_temp)
	return(new_data)

def sum_text(vecteur_text):
	output = ''
	for word in vecteur_text:
		output = output +' '+ word
	return(output)

def data_reshape(data,type_of_query):
	common_list = ['the','a','this','another','please','.','?',',','can','you','an','me',"I'd",'I','want','wanted','would','like'] 
	dico_stop_words ={'AddToPlaylist' : common_list
					  , 'GetWeather' : common_list ,'RateBook':common_list, 'PlayMusic' :common_list, 
					  'PlayMusic' : common_list, 'SearchScreeningEvent': common_list}
	queries_entity = []
	future_df = []
	
	for query_id, query in enumerate(data):
		temp = ''
		temp_entity = []
		for row in query:
			temp_future = [query_id]
			temp_future.append(row['text'].lower())
			if 'entity' in row.keys():
				temp_entity.append(row['entity'])
				temp_future.append(row['entity'])
			else :
				temp_future.append('None')
			if '' in temp_future:
				temp_future.remove('')
			future_df.append(temp_future)
	
	df = pd.DataFrame(future_df, columns=['query_id','text','entity'])
	df.dropna(subset = ['text','entity'], inplace = True)
	
	#We remove here stop words specificaly for each type of query
	df = df[~df.text.isin(dico_stop_words[type_of_query])]
	
	queries = df.groupby('query_id').apply(lambda x : sum_text(x.text))
		
	return({'queries_entity': queries_entity,'df':df})

def add_col(df):
	query_id = 0
	entity_before = ''
	entity_before_list = []
	for index, row in df.iterrows():
		if row.query_id == query_id :
			entity_before_list.append(entity_before)
		else :
			entity_before = ''
			entity_before_list.append(entity_before)
			query_id = row.query_id
		entity_before = row.entity
	return(entity_before_list)

def text_to_proba(text, which,proba):
	which_list = {'before': '_before' ,'after': '_after', 'itself' : ''}
	all_queries_entity = ['None', 'music_item', 'playlist', 'artist', 'playlist_owner', 'entity_name']
	proba_dict = { entity : [proba[proba.text == text]['number_'+entity+which_list[which]].iloc[0]  ,  int(proba[proba.text == text]['occurence_number'].iloc[0])] if len(proba[proba.text == text]) > 0 else [0,0] for entity in all_queries_entity }

	return(proba_dict )

def multiply(before,itself,after,alpha,beta,gamma):
	new_dic = {}
	list_keys = np.unique(list(before.keys()) + list(itself.keys()) + list(after.keys()))
	
	if before == {}:
		before = {clef : [0,0] for clef in before.keys()}
		
	if itself == {}:
		itself = {clef : [0,0] for clef in before.keys()}
		
	if after == {}:
		after = {clef : [0,0] for clef in before.keys()}
		
	for key in before.keys():
		sum_occurence = before[key][1] + itself[key][1] + after[key][1]
		 
		if sum_occurence == 0: #I don't want to divide by zero line 22
			sum_occurence = 1
			
		new_dic[key] = (alpha * before[key][0] * before[key][1]  + beta*itself[key][0]*itself[key][1] + gamma*after[key][0]*after[key][1])/sum_occurence

	if list(max_value(itself).values())[0] >0.90:
		new_dic = max_value(itself)
		
	return(new_dic)


def max_value(dico):
	max_value = 0
	max_key = 0
	for key,value in dico.items():
		if value[0] > max_value:
			max_value = value[0]
			max_key = key
	return({max_key : max_value})    


def key_max_value(dico):
	max_value = 0
	max_key = ''
	for key, value in dico.items():
		if value > max_value:
			max_key = key
			max_value = value
	return(max_key)


def word_to_test_to_demo(query,type_of_query):
	common_list = ['the','a','this','another','please','.','?',',','can','you','an','me',"I'd",'I','want','wanted','would','like'] 
	dico_stop_words ={'AddToPlaylist' : common_list
					  , 'GetWeather' : common_list ,'RateBook':common_list, 'PlayMusic' :common_list, 
					  'PlayMusic' : common_list, 'SearchScreeningEvent': common_list}
	word_tokens = query.split(' ')
	word_tokens = [word_token if word_token not in dico_stop_words[type_of_query] else 'None' for word_token in word_tokens]
   
	dict_output = {}
	for index,word in enumerate(word_tokens):
		if index == 0:
			output = key_max_value(  multiply(text_to_proba(word_tokens[index+1],'before',proba),text_to_proba(word,'itself'),{},alpha,beta,gamma))
		if index == len(word_tokens)-1:
			output = key_max_value(multiply( text_to_proba(word_tokens[index-1],'before')  ,text_to_proba(word,'itself'), {},alpha,beta,gamma ))
		elif (index >0) & (index < len(word_tokens)-1) :
			output = key_max_value(multiply(text_to_proba(word_tokens[index+1],'before'),text_to_proba(word,'itself'),text_to_proba(word_tokens[index-1],'after'),alpha,beta,gamma))

		dict_output[word] = output
   
	to_return = [{word : dict_output[word]} if word in dict_output.keys() else {word : 'None'} for word in query.split(' ')]

	return(to_return)


def word_to_test(query,proba):
	alpha =1
	beta =2
	gamma = 0.2
	word_tokens = query
	vecteur = []
	vecteur_word = []
	
	for index,word in enumerate(word_tokens):
		if index == 0:
			output = key_max_value(  multiply(text_to_proba(word_tokens[index+1],'before',proba),text_to_proba(word,'itself',proba),{},alpha,beta,gamma))
		if index == len(word_tokens)-1:
			output = key_max_value(multiply( text_to_proba(word_tokens[index-1],'before',proba)  ,text_to_proba(word,'itself',proba), {},alpha,beta,gamma ))
		elif (index >0) & (index < len(word_tokens)-1) :
			output = key_max_value(multiply(text_to_proba(word_tokens[index+1],'before',proba),text_to_proba(word,'itself',proba),text_to_proba(word_tokens[index-1],'after',proba),alpha,beta,gamma))
		vecteur_word.append(word)    
		vecteur.append(output)
		
	return([vecteur_word,vecteur])


def df_predict_bis(df_test,alpha,beta,gamma):
	entity_test = []
	queries_df = df_test.groupby('query_id')

	for query_id, group in queries_df:
		entity_test += word_to_test(list(group.text),proba)[1]

	df_test['entity_test'] = entity_test
	df_test['prediction'] = df_test.apply(lambda row : row.entity == row.entity_test,axis = 1)

	return(df_test)


def df_predict(df_test,proba,alpha,beta,gamma):
	all_queries_entity = ['None', 'music_item', 'playlist', 'artist', 'playlist_owner', 'entity_name']
	entity_test = []
	queries_df = df_test.groupby('query_id')

	for query_id, group in queries_df:
		entity_test += word_to_test(list(group.text),proba)[1]

	df_test['entity_test'] = entity_test
	df_test['prediction'] = df_test.apply(lambda row : row.entity == row.entity_test,axis = 1)
	grouped = df_test.groupby('query_id').apply(lambda x : 1 if sum(x.prediction)/len(x) ==1 else 0).reset_index(name = 'number')
	wrong_entity_rate = sum(grouped.number)/len(grouped)
	wrong_query_rate = sum(df_test.prediction)/len(df_test)
	
	vanity_metric = df_test.groupby('query_id').apply(lambda x : pd.Series({
	'query_type' : list(x[x.entity != 'None'].entity.unique()) ,
	'query_type_test' : list(x[x.entity_test != 'None'].entity_test.unique()) ,
	'query' : sum_text(x.text)
								} )).reset_index()
	vanity_metric['prediction'] = vanity_metric.apply(lambda row : row.query_type == row.query_type_test , axis =1 )
	vanity_metric = sum(vanity_metric.prediction)/len(vanity_metric)

	return([wrong_entity_rate,wrong_query_rate,vanity_metric])