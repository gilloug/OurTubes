#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def main(mysql = None, connected='False', connected_as="", connected_to="", login="", password=""):
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Player</title>
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
        <li><a class="red-text accent-4 active" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
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
    <div class="row collection">"""
    if connected == "True" and connected_as == "Administrator":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('getPlaylist', [connected_to])
        data = cursor.fetchall()
        data = tuple(sorted(data, reverse=True, key=lambda item: item[5]))
        conn.commit()
        conn.close()
        if len(data) is not 0:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('playMusic', [connected_to, data[0][2]])
            conn.commit()
            conn.close()
            _id = (data[0][2]).split("https://www.youtube.com/watch?v=")[1]
            ret += """
            <div class="center-align" id="player"></div>
            <script>
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            var player;
            function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
            videoId: \"""" + _id + """\",
            events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
            }
            });
            }
            function onPlayerReady(event) {
            event.target.playVideo();
            }
            var done = false;
            function onPlayerStateChange(event) {
            if(event.data === 0) {
            $.ajax({
            url: '/changeMusic',
            type: 'POST',
            success: function(response) {
            location.reload();
            },
            error: function(error) {
            Materialize.toast('ERROR While changing music', 4000, 'red')
            }
            });
            }
            }
            function stopVideo() {
            player.stopVideo();
            }
            </script>"""
        else:
            ret += """<p class="center-align"><b><i>Add musics first</i></b></p>"""
    else:
        ret += """<p class="center-align"><b><i>Join a channel</i></b></p>"""
    ret += """</div>
    <div class="fixed-action-btn" style="bottom:74px; right:15px">
    <a class="btn-floating btn-large waves-effect waves-light green accent-5" id="next" name="next"><i class="material-icons">skip_next</i></a>
    </div>
    <script>
    $(function() {
    $('#next').click(function(e) {
    $.ajax({
    url: '/changeMusic',
    type: 'POST',
    success: function(response) {
    location.reload();
    },
    error: function(error) {
    Materialize.toast('ERROR While changing music', 4000, 'red')
    }
    }); }); }); </script>
    <footer class="page-footer red accent-5>
    <div class="footer-copyright">
    <p class="center">&copy; BunnyCompany 2018</p>
    </div>
    </footer>
    </body>
    </html>"""
    return ret
