#Run the app
install -r requirements.txt

cd webapp_js/

python main.py

#Direct to app

http://localhost:5000


#if this did not work (blank page) (sometimes it doesn't work based off of weird windows MIME types)
ctrl+c to stop the server

cd webapp_mjs/

python main.py

#direct to app

http://localhost:5000


# there is a list of test data and you can click on the rows and see what my models predict that headline to be (type wise)

# You also have a choice to input your own headline and see what my models think the type of article is
