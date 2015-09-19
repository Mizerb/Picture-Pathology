from imgurpython import ImgurClient

client_id = '################'
client_secret = '#############################'

client = ImgurClient(client_id, client_secret)
target = open("test.txt", 'w')


# Example request

for i in range(10):

	items = client.gallery(section='hot', sort='viral', page=i, window='day', show_viral=True)

	for item in items:
		if ".jpg" in item.link:
			target.write(str(item.link))
			target.write("\n")
			print item.link

			
target.close()