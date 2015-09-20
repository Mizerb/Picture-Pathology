from imgurpython import ImgurClient

client_id = '51a86b471a85443'
client_secret = '442df4f265e082d2c168ad2ea7da3607b12b37e8'
target_file = str(sys.argv[1])



client = ImgurClient(client_id, client_secret)
target = open(target_file, 'w')


# Example request

for i in range(10):

	items = client.gallery(section='hot', sort='viral', page=i, window='day', show_viral=True)

	for item in items:
		if ".jpg" in item.link:
			target.write(str(item.link))
			target.write("\n")
			print item.link

			
target.close()