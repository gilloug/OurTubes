#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def result(data=None):
    i = 0
    ret = """<ul class="collection">"""
    if data and len(data) is not 0:
        for music in data:
            ret += """<li class="collection-item avatar">
            <img src=\"""" + music[0] + """\" alt="" class="square">
            <a class="title" href=\"""" + music[2] + """\">""" + music[1] + """</a>
            <div class="secondary-content">
            <a id="addBtn""" + str(i) + """\" data-title=\"""" + music[1] + """\" data-picture=\"""" + music[0] + """\" data-url=\"""" + music[2] + """\" class = "btn-floating waves-effect waves-light green">
            <i id="addBtn""" + str(i) + """\" class = "material-icons">add</i></a>
            <script>
            $(function() {
            $('#addBtn""" + str(i) + """\').click(function(e) {
            e.stopImmediatePropagation();
            var picture = $(this).data('picture');
            var title = $(this).data('title');
            var url = $(this).data('url');
            $.ajax({
            url: '/addMusic',
            data: {'picture': picture, 'title': title, 'url': url},
            type: 'POST',
            success: function(response) {
               window.location.href = "index";
            },
            error: function(error) {
               Materialize.toast('Chan cannot be created', 4000, 'red')
            }
            });
            });
            });
            </script></div></li>"""
            i += 1
    ret +="</ul>"
    return ret

def main(connected='False', connected_as='', connected_to=''):
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Add Music</title>
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
    }); }); });</script>"""
    if connected_as == "Administrator":
        ret += """<li class="divider"></li>
        <li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
    ret += """</ul>
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
    </nav>"""
    if connected == "True":
        ret += """<form class="form-signin container">
        <label for="search" class="sr-only">Music name</label>
        <input type="text" name="search" id="search" class="form-control" placeholder="music name" required autofocus>
        <button id="btnSearch" class="btn btn-lg btn-primary btn-block" type="button">Search</button>
        <script>
        $(function() {
        $('#btnSearch').click(function() {
        $.ajax({
        url: '/searchMusicParam',
        data: $('form').serialize(),
        type: 'GET',
        success: function(response) {
        $(response).appendTo(".inner");
        },
        error: function(error) {
        }
        });
        });
        });
        </script>
        </form>
        <div class="inner container"><div>
        """
    else:
        ret += """<p class="center-align"><b><i>Join a channel</i></b></p>"""
    ret += """<footer class="page-footer red accent-5>
    <div class="footer-copyright">
    <p class="center">&copy; BunnyCompany 2018</p>
    </div>
    </footer>
    </body>
    </html>"""
    return ret
