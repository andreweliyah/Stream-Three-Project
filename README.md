# Stream Three Project
This is my final project for Code Institute Stream Three. The Example page can be found here: https://blogreaderpro.herokuapp.com

Please note this is merely a course project, and any information obtained from this app will be used for that purpose and only that purpose. With that said, I urge that you please do not use your actual payment or contact information on the demo site. If you do want to test it out please use a fake email (Johnsmith@example.com) and the stripe test card number (4242 4242 4242 4242).

## Summary
This project is used to demonstrate my working knowledge of the course. Things such as the Django web framework, Dango Rest API framework, and Django JWT framework. As well as demonstrating knowledge of things I've learned in previous course sections. Things such as data visualization with DC.JS, crossfilter and D3.JS. and database usage, plus stripe integration with backend code and the stripe checkout widget, site hosting, and git usage among other things. 

This app uses sqlite for dev and mysql for staging environments.

This app is called DevTracker, and is used to keep track of developers of a blog reading app called Blog Reader Pro. Users can login, submit bug tickets for issues that they have found in the app, feature tickets for features that they would like to see in the app, as well as being able to vote and comment on those tickets.

There is also an optional subscription service to unlock the ability to vote on and submit feature tickets, bugs are always free to submit, comment and vote on. This is done in the settings under subscription with the pay button.

There is also a blog for the developers to use to keep their users up-to-date. The profile page shows all the activity of the user. The main DevTracker or page is used for data visualization. Showing the average ticket completion for days weeks and months. A pie chart showing the percentage of completed tickets by type of ticket (bug or feature) to data tables showing the top five voted on features and bugs and finally a data table that shows the complete list of tickets regardless of status or type. Users can click on the link and be taken to the detail page of any ticket where they can comment or vote on it as long as they have the proper prescription for the ticket type.

## Technologies
- HTML
- CSS
- Javascript
- JQuery
- DC.js
- Crossfilter.js
- D3.js
- Python
- Django
- Django Rest Framework
- Djanto JWT Framework
- Stripe payment system
- MySQL
- Bootstrap 4
- Heroku (for hosting)

## Installation 

```bash
$ git clone https://github.com/andreweliyah/Stream-Three-Project.git

$ cd Stream-Three-Project

$ pip install -r requirements.txt 

```
Add your stripe keys to settings/dev.py or settings/staging.py depending on your needs.
Next run migrations 
```bash
$ python manage.py migrate
```
And run the app 
Dev:
```
$ python manage.py runserver --settings=settings.dev
```
Staging (this is only really used by Heroku):
```
$ python manage.py runserver --settings=settings.staging
```
## Testing
I used the standard Django unit testing for this project to test all my models.
To run them:
```
$ python manage.py test
```

This it hope you enjoy.