<h1 align="center">
	<a href="http://www.speakerfight.com/events"><img src="http://i.imgur.com/cDfy85g.png" alt="Speakerfight" width="75%"></a>
	<br>
	The Easier way to choose the best talks.
	<br>
	<p align="center">
	  <a href="https://gitter.im/luanfonceca/speakerfight"><img src="https://badges.gitter.im/Join%20Chat.svg" alt="Gitter"></a>
	  <a href="https://circleci.com/gh/luanfonceca/speakerfight/tree/master"><img src="https://circleci.com/gh/luanfonceca/speakerfight.svg?style=shield"></a>
	  <a href="https://landscape.io/github/luanfonceca/speakerfight/master"><img src="https://landscape.io/github/luanfonceca/speakerfight/master/landscape.svg?style=flat"></a>
	  <a href="https://coveralls.io/r/luanfonceca/speakerfight?branch=master"><img src="http://img.shields.io/coveralls/luanfonceca/speakerfight.svg?branch=master"></a>
	 	<a href="http://waffle.io/luanfonceca/speakerfight" target="_blank"><img src="https://img.shields.io/waffle/label/luanfonceca/speakerfight/ready.svg?style=flat&label=Roadmap"></a>
	</p>
	<br>
</h1>

<h2>How to Contribute</h2>
<blockquote>
	In case if you want to contribute with code, I recomend you to look at our <a href="https://github.com/luanfonceca/speakerfight/milestones" target="_blank">Roadmap</a>. In that section you will find many issues to help us to keep on track of an awesome project timeline.
	<br>
	See our <a href="https://github.com/luanfonceca/speakerfight/blob/master/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a> file to understand how we code.
</blockquote>
<h3>
	<ul>
		<li>
			<a href="https://waffle.io/luanfonceca/speakerfight" target="_blank">
				Roadmap Issues
			</a>
		</li>
		<li>Review Pull Requests</li>
		<li>Review Issues</li>
		<li>Blogposts</li>
	</ul>
</h3>

<h2>How to Install</h2>
<blockquote>
	After installation, you will have two users created "admin:admin" and "user:user". In order to use the Social Authentication you need to setup the <a href="https://github.com/pennersr/django-allauth">django-allauth</a> by yourself, for security reasons.
</blockquote>

<h3>Normal Installation</h3>

```sh
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ make setup
$ python manage.py runserver
```

<h3>Docker Installation</h3>
<h4>
	<h5>Dependencies:</h5>
	<ul>
		<li><a href="https://www.docker.com" target="_blank">Docker</a></li>
		<li><a href="https://docs.docker.com/compose" target="_blank">Docker compose</a></li>
	</ul>
</h4>

```sh
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ docker-compose build
$ docker-compose run web make setup
$ docker-compose up
```

