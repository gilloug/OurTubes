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
    <script>
      $( document ).ready(function() {
      $(".button-collapse").sideNav();
      });
    </script>
    <nav>
      <div class="nav-wrapper red accent-4">
	<a href="/" class="brand-logo">OurTubes</a>
	<ul id="slide-out" class="side-nav">
	  <li class="no-padding">
            <ul class="collapsible collapsible-accordion">
	      <li>
		<a class="collapsible-header green accent-3">Channels<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>
                    <li><a href="createChan">create</a></li>
                    <li><a href="deleteChan">delete</a></li>
                    <li><a href="joinChan">join</a></li>
<li><a id="leave" name="leave" href="#!">leave</a></li>
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
	<li class="green"><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
    ret += """</ul>
		</div>
	      </li>
 	      <li>
		<a class="collapsible-header">Account<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>
                    <li><a id="logout" name="logout" href="#!">Log out</a></li>
		    <script>
		      $(function() {
		      $('#logout').click(function(e) {
		      $.ajax({
		      url: '/logout',
		      type: 'POST',
		      success: function(response) {
		      window.location.href = "index";},
		      error: function(error) {}
		      }); }); });
		    </script>
		  </ul>
		</div>
	      </li>
	      <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i>Help</a></li>
            </ul>
	  </li>
	</ul>
	<ul class="right hide-on-med-and-down">
	  <li class="active">
	    <a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown1">Channels<i class="material-icons right">arrow_drop_down</i></a>
	    <ul  id='dropdown1' class='dropdown-content'>
              <li><a href="createChan" class="black-text">create</a></li>
              <li><a href="deleteChan" class="black-text">delete</a></li>
              <li><a href="joinChan" class="black-text">join</a></li>
<li><a id="lve" name="lve" href="#!" class="black-text">leave</a></li>
    <script>
    $(function() {
    $('#lve').click(function(e) {
    $.ajax({
    url: '/leave',
    type: 'POST',
    success: function(response) {window.location.href = "index";},
    error: function(error) {}
    }); }); });</script>"""
    if connected_as == "Administrator":
        ret += """<li class="divider"></li>
	      <li class="active"><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
    ret += """</ul>
	  <li>
	    <a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown2">Account<i class="material-icons right">arrow_drop_down</i></a>
	    <ul  id='dropdown2' class='dropdown-content'>
              <li><a id="lgt" name="lgt" href="#!" class="black-text">Log out</a></li>
	      <script>
	  	$(function() {
	  	$('#lgt').click(function(e) {
	  	$.ajax({
	  	url: '/logout',
	  	type: 'POST',
	  	success: function(response) {
	  	window.location.href = "index";},
	  	error: function(error) {}
	  	}); }); });
	      </script>
	    </ul>
	  </li>
	  <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text left">help_outline</i>Help</a></li>
	</ul>
	<a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
      </div>
    </nav>
    """
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
    ret += """
    <div class="fixed-action-btn" style="bottom:15px; right:15px">
    <a class="btn-floating btn-large waves-effect waves-light green accent-4" id="next" name="next"><i class="material-icons">skip_next</i></a>
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
    </body>
    </html>"""
    return ret
