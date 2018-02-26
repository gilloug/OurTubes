#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def connection():
    ret = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Log In</title>
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
                <a class="collapsible-header green accent-3">Account<i class="material-icons">arrow_drop_down</i></a>
                <div class="collapsible-body">
                  <ul>
                    <li><a href="register">Sign in</a></li>
                    <li class="green"><a href="index">Log in</a></li>
                  </ul>
                </div>
              </li>
              <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text">help_outline</i>Help</a></li>
            </ul>
          </li>
        </ul>
        <ul class="right hide-on-med-and-down">
            <li class="active"><a class="dropdown-button" href="#!" data-hover="true" data-belowOrigin="true" data-activates="dropdown2">Account<i class="material-icons right">arrow_drop_down</i></a>
            <ul id='dropdown2' class='dropdown-content'>
               <li><a href="register">Sign in</a></li>
               <li class="active"><a href="index">Log in</a></li>
            </ul>
          <li><a class="blue-text accent-4" href="help"><i class="material-icons blue-text left">help_outline</i>Help</a></li>
        </ul>
</li>
        <a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
      </div>
    </nav>
    </div>
    <div class="container">
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
		<a class="collapsible-header">Channels<i class="material-icons">arrow_drop_down</i></a>
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
	<li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
    ret += """</ul>
    </div>
	      </li>
 	      <li class="active">
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
	  <li>
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
	<li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
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
    </div>
    <ul class="collection">"""
    if connected == "True":
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('getPlaylist', [connected_to])
        data = cursor.fetchall()
        i = 0
        data = tuple(sorted(data, reverse=True, key=lambda item: item[5]))
        if len(data) <= 0:
            ret += """<li class="collection-item avatar">
            <img src="https://cdn4.iconfinder.com/data/icons/vectory-bonus-3/40/channel_rss-256.png" alt="" width="100" height="100" class="">
            <p>
            Current Channel:
            <br/>
            <a>""" + connected_to + """</a>
            </p>"""
        if len(data) is not 0:
            for music in data:
                if i == 0:
                    ret += """<li class="collection-item avatar">
                    <img src="https://cdn4.iconfinder.com/data/icons/vectory-bonus-3/40/channel_rss-256.png" alt="" width="100" height="100" class="">
                    <p>
                    Current Channel:
                    <br/>
                    <a>""" + connected_to + """</a>
                    </p>"""
                    ret += """<li class="collection-item avatar">
                    <img src=\"""" + music[3] + """\" alt="" class="">
                    <p>
                    Current music:
                    <br/>
                    <a>""" + music[4] + """</a>
                    </p>"""
                if i != 0:
                    ret += """<li class="collection-item avatar">
                    <img src=\"""" + music[3] + """\" alt="" class="">
                    <p>
                    <a class="title" href=\"""" + music[2] + """\">""" + music[4] + """</a>
                    <br/>
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
                        ret += """<br/><a id="deleteBtn""" + str(i) + """\" data-url=\"""" + music[2] + """\" class = "btn-floating waves-effect waves-light red accent-4 right">
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
        </div></li>
        <li class="collection-item avatar">
        <p><br/></p>
        </li>
        </ul>"""
        conn.commit()
        conn.close()
    else:
        ret += """<p class="center-align"><b><i>Join a channel</i></b></p>"""
    ret += """</ul>
 </div>
    <div class="fixed-action-btn" style="bottom:15px; right:15px">
    <a class="btn-floating btn-large waves-effect waves-light green accent-4" id="refresh" name="refresh"><i class="material-icons">refresh</i></a>
    </div>
    <script>
    $(function() {
    $('#refresh').click(function(e) {
    location.reload();
    }); }); </script>
    </body>
    </html>"""
    return ret
