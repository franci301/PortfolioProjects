pushing

git add .
git commit -am 'msg'
git push heroku master

starting 
heroku login
heroku ps:scale web=1

logs
heroku logs --tail