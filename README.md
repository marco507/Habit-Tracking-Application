# Habit Tracker : Simple command line habit tracking application

## Overview
Habit Tracker is a simple command line application for managing and analyzing self-defined periodic habits. The application features a clean command line interface and is controlled by calling functions with their respective arguments, much like well known UNIX tools, for example grep. It runs on a lightweight relational database stored in a single file, so no need to set-up a full SQL server.

## Features
* Create and manage self defined habits
* Support for a daily and weekly period
* Analyze habits with the built-in analytics module
* Allows multiple users
* Clean command line interface
* Lightweight relational database in a single file
* Intergrated unit test suite 

## Installation
To use the habit tracker you need an installation of Python 3.9.0.
To install:
1. Download the application package from Github and extract the contents.
2. Install `pipenv` with `pip install pipenv` if you don't have it already installed.
3. Open a command prompt in the extracted folder and execute `pipenv install` to install the dependencies.
4. Run `pipenv shell` to enter the new virtual environment
5. You are ready to use the habit tracker

## Usage
For using the habit tracker refer to the manual which is contained in the application package.

## Dependencies
* Fire
* Pandas

## License
GPL-3.0 License
