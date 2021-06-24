protein_domains_vs_string_degree.png :  filtered_protein_interactions.txt protein_w_domains.txt
	python create_network.py filtered_protein_interactions.txt protein_w_domains.txt protein_domains_vs_string_degree.png 

filtered_protein_interactions.txt : protein_interactions.txt.gz
	gzip -d protein_interactions.txt.gz --stdout | awk '$$3>=500 {print ;}' > filtered_protein_interactions.txt

protein_interactions.txt.gz : 
	wget https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz -O protein_interactions.txt.gz	

protein_w_domains.txt : 
	wget -L https://stockholmuniversity.app.box.com/shared/static/n8l0l1b3tg32wrzg2ensg8dnt7oua8ex -O protein_w_domains.txt

 
	   
	





	
