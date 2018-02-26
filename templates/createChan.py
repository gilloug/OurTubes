#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def main(mysql=None, connected_as=''):
    ret = """ """
    ret += """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link rel="stylesheet" type="text/css" href="style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Create Channel</title>
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
		<a class="collapsible-header green accent-4">Channels<i class="material-icons">arrow_drop_down</i></a>
		<div class="collapsible-body">
		  <ul>
                    <li class="active green"><a href="createChan">create</a></li>
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
    }); }); });</script>
		    <li class="divider"></li>"""
    if connected_as == "Administrator":
        ret += """<li><a class="red-text accent-4" href="player"><i class="material-icons red-text">play_arrow</i>Player</a></li>"""
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
              <li class="active"><a href="createChan" class="black-text">create</a></li>
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
    </ul>
    <div class="container">
      <form class="form-signin">
        <label for="inputChanName" class="sr-only">Chan name</label>
        <input type="text" name="inputChanName" id="inputChanName" class="form-control" placeholder="Chan name" required autofocus>
        <label for="inputPublicPassword" class="sr-only">Public Password</label>
        <input type="password" name="inputPublicPassword" id="inputPublicPassword" class="form-control" placeholder="Password" required>
	<label for="inputPrivatePassword" class="sr-only">Private Password</label>
        <input type="password" name="inputPrivatePassword" id="inputPrivatePassword" class="form-control" placeholder="Password" required>
	<button id="btnCreate" class="btn btn-lg btn-primary btn-block" type="button">Create</button>
	<script>
	  $(function() {
	  $('#btnCreate').click(function() {
          $.ajax({
          url: '/create',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
          Materialize.toast('Chan created', 3000, 'green')
          function show_popup(){
          location.reload();
          };
          window.setTimeout( show_popup, 3000 );
          },
          error: function(error) {
	  Materialize.toast('Chan cannot be created', 4000, 'red')
          }
          });
	  });
	  });
	</script>
    <br/><br/>
      </form>
    </div>"""
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('getChans')
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    i = 0
    ret += """<ul class="collection container">"""
    if data and len(data) is not 0:
        for chan in data:
            if i == 0:
                ret += """<li class="divider"></li>
                <li class="collection-item">
                <p class="center-align"><b><i>Existing channels:</i></b></p></li>"""
            ret += """<li class="collection-item center">""" + chan[1] + """</li>"""
            i += 1
    ret += """</body>
    </html>"""
    return ret
