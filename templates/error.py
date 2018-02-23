#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def login(mysql = None):
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Error</title>
    </head>
    <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <nav class="red accent-4">
<ul class="nav nav-pills pull-right">
    <li role="presentation" class="active"><a href="/">OurTubes</a></li>
    <li><a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown1">Channels<i class="material-icons right">arrow_drop_down</i></a></li>
    <ul id='dropdown1' class='dropdown-content'>
    <li><a class="black-text center-align" href="createChan">Create</a></li>
    <li><a class="black-text center-align" href="deleteChan">Delete</a></li>
    <li><a class="black-text center-align" href="joinChan">Join</a></li>
    <li><a class="black-text center-align" id="leave" name="leave" href="#!">Leave</a></li>
    <script>
    $(function() {
    $('#leave').click(function(e) {
    $.ajax({
    url: '/leave',
    type: 'POST',
    success: function(response) {window.location.href = "index";},
    error: function(error) {}
    }); }); });</script>
    </ul>
    <li class="right"><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i></a></li>
    <li><a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown2">Account<i class="material-icons right">arrow_drop_down</i></a></li>
    <ul id='dropdown2' class='dropdown-content'>
    <li><a id="logout" name="logout" class="black-text center-align" href="#!">Logout</a></li>
    <script>
    $(function() {
    $('#logout').click(function(e) {
    $.ajax({
    url: '/logout',
    type: 'POST',
    success: function(response) {
    window.location.href = "index";},
    error: function(error) {}
    }); }); }); </script>
    </ul>
    </ul>
    </nav>
    <div class="row collection">
    <p class="center-align"><b><i>Log in</i></b></p>
    </div>
    <footer class="footer">
    <p>&copy; BunnyCompany 2018</p>
    </footer>
    </body>
    </html>"""
    return ret
