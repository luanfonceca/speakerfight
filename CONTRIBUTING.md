# Contributing to Speakerfight

We'd love your contribution to our project and to make Speakerfight. Here are the guidelines we'd like you to follow:

- [Issues and Bugs](#issues-and-bugs)
- [Submission Guidelines](#submission-guidelines)
- [Coding Rules](#coding-rules)


## Issues and Bugs

If you find a bug in the source code or a mistake in the documentation, you can help us by
submitting an issue to our [GitHub repository][speakerfight]. Even better you can submit a pull request
with a fix.

## Submission Guidelines

### Submitting an Issue

Before you submit your issue search the archive, maybe your problem was already answered.
Also check if there is no work in progress to fix your problem (when no issue to the problem was created).

### Submitting a pull request

Building the environment:

```
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ make setup
$ python manage.py runserver
```

Before you submit your pull request consider the following guidelines:

* Make your changes in a new branch:

	```sh
	git checkout -b my-fix-branch master
	```

* Follow our [Coding Rules](#coding-rules).
* Run the test suite:

	```sh
	python manage.py test
	```

* Run code coverage:

	```sh
	coverage run manage.py test
	```

* Commit your work, including appropriate test cases (unit tests, functional tests, regression tests, etc).
* When commiting remember to write clear commit messages explaining why the change is important.
* Run the test suite to ensure your code is working properly.
* Push to the upstream and create a pull request against the master branch.

## Coding Rules

To ensure consistency throughout the source code, keep the following rules in mind:

* Speakerfight follows the same conventions [Django][django-coding-style] uses.
* Some programming languages have their own coding style guide. [EditorConfig][editorconfig] is here to help us on this.
* All features or changes must be tested (your patch should have tests proving your code works as expected).
* Code coverage is important.

[speakerfight]: https://github.com/luanfonceca/speakerfight/
[editorconfig]: http://editorconfig.org/
[django-coding-style]: https://docs.djangoproject.com/en/1.8/internals/contributing/writing-code/coding-style/
