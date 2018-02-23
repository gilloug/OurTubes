#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def connection():
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Log In</title>
    </head>
    <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <div class="navbar-fixed">
    <nav class="red accent-4">
    <ul class="nav nav-pills pull-right">
    <li role="presentation" class="active"><a href="#!">OurTubes</a>
    </li>
    <li class="right"><a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown0">Account<i class="material-icons right">arrow_drop_down</i></a></li>
    <ul id='dropdown0' class='dropdown-content'>
    <li><a href="register">Sign in</a></li>
    <li class="active"><a href="index">Log in</a></li>
    </ul>
    <li class="right"><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i></a></li>
    </ul>
    </nav>
    </div>
    <div class="col s6 pull-s6 container jumbotron">
    <form class="form-signin">
    <label for="inputChanName" class="sr-only">email</label>
    <input type="email" name="inputEmail" id="inputEmail" class="form-control" placeholder="email" required autofocus>
    <label for="inputPassword" class="sr-only">Password</label>
    <input type="password" name="inputPassword" id="inputPassword" class="form-control" placeholder="password" required>
    <button id="btnLogin" class="btn btn-lg btn-primary btn-block" type="button">Login</button>
    <script>
    $(function() {
    $('#btnLogin').click(function() {
    $.ajax({
    url: '/connect',
    data: $('form').serialize(),
    type: 'POST',
    success: function(response) {
    location.reload();
    },
    error: function(error) {
    Materialize.toast('Cannot login', 4000, 'red')
    }
    });
    });
    });
    </script>
    </form>
    </div>
    </body>
    <footer class="page-footer red accent-5>
    <div class="footer-copyright">
    <p class="center">&copy; BunnyCompany 2018</p>
    </div>
    </footer>
    </html>"""
    return ret

def main(mysql = None, connected='False', connected_as="", connected_to="", login="", password=""):
    if login == "" or login == None:
        return connection()
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <link rel="stylesheet" type="text/css" href="style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes</title>
    </head>
    <body>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <div class="navbar-fixed">
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
    </nav>
    </div>
    <div class="row collection">"""
    if connected == "True":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('getPlaylist', [connected_to])
        data = cursor.fetchall()
        i = 0
        data = tuple(sorted(data, reverse=True, key=lambda item: item[5]))
        if len(data) > 0:
            ret += """<li class="collection-item avatar">
            <div class="title">
            Current channel: """ + connected_to + """
            </div>
            <div class="secondary-content">
            Current music: """ + data[0][4] + """
            </div>
            </li>"""
        else:
            ret += """<li class="collection-item">
            <p class="title">
            Current channel: """ + connected_to + """
            </p>
            </li>"""
        if len(data) is not 0:
            for music in data:
                if i != 0:
                    ret += """<li class="collection-item avatar">
                    <img src=\"""" + music[3] + """\" alt="" class="circle">
                    <a class="title" href=\"""" + music[2] + """\">""" + music[4] + """</a>
                    <p>
                    """ + str(music[5]) + """ Likes
                    </p>
                    <div class="secondary-content">
                    <a id="upBtn""" + str(i) + """\" data-url=\"""" + music[2] + """\" class="btn-floating waves-effect waves-light green accent-4">
                    <i id="upBtn""" + str(i) + """\" class="material-icons">arrow_drop_up</i></a>
                    <script>
                    (function( $ ){
                    $.fn.endfunction = function() {
                    alert('hello world');
                    return this;
                    };
                    })( jQuery );
                    $(function() {
                    $('#upBtn""" + str(i) + """\').click(function(e) {
                    e.stopImmediatePropagation();
                    var url = $(this).data('url');
                    $.ajax({
                    url: '/upvoteMusic',
                    data: {'url': url},
                    type: 'POST',
                    success: function(response) {
                    location.reload();
                    },
                    error: function(error) {
                    }
                    });
                    });
                    });
                    </script>
                    <a id="downBtn""" + str(i) + """\" data-url=\"""" + music[2] + """\" class = "btn-floating waves-effect waves-light green accent-4">
                    <i id="downBtn""" + str(i) + """\" class = "material-icons">arrow_drop_down</i></a>
                    <script>
                    $(function() {
                    $('#downBtn""" + str(i) + """\').click(function(e) {
                    e.stopImmediatePropagation();
                    var url = $(this).data('url');
                    $.ajax({
                    url: '/downvoteMusic',
                    data: {'url': url},
                    type: 'POST',
                    success: function(response) {
                    location.reload();
                    },
                    error: function(error) {
                    }
                    });
                    });
                    });
                    </script>"""
                    if (connected_as == "Administrator"):
                        ret += """<a id="deleteBtn""" + str(i) + """\" data-url=\"""" + music[2] + """\" class = "btn-floating waves-effect waves-light red accent-4">
                        <i id="deleteBtn""" + str(i) + """\" class = "material-icons">delete</i></a>
                        <script>
                        $(function() {
                        $('#deleteBtn""" + str(i) + """\').click(function(e) {
                        e.stopImmediatePropagation();
                        var url = $(this).data('url');
                        $.ajax({
                        url: '/deleteMusic',
                        data: {'url': url},
                        type: 'POST',
                        success: function(response) {
                        location.reload();
                        },
                        error: function(error) {
                        }
                        });
                        });
                        });
                        </script>"""
                    ret += """</div></li>"""
                i += 1
        ret += """<li class="collection-item avatar">
        <img src="http://articleimage.nicoblomaga.jp/image/258/2018/0/d/0d46bec0cb350a8903af8e4564530580a1f1b1591519124974.png" alt="" class="circle">
        <a class="title">YouTube</a>
        <p>Add a music from YouTube</p>
        <div class="secondary-content">
        <a id="addBtn" href="searchMusic" class="btn-floating waves-effect waves-light green accent-4">
        <i id="addBtn" class="material-icons">add</i></a>
        </div></li></ul>"""
        conn.commit()
        conn.close()
    else:
        ret += """<p class="center-align"><b><i>Join a channel</i></b></p>"""
    ret += """</div>
    <footer class="page-footer red accent-5>
    <div class="footer-copyright">
    <p class="center">&copy; BunnyCompany 2018</p>
    </div>
    </footer>
    </body>
    </html>"""
    return ret
