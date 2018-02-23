#!/usr/bin/env python3

import sys
from flask import Flask, render_template, request, json, jsonify

def main(mysql=None, connected_as=''):
    ret = """ """
    ret += """<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="icon" type="image/png" href="favicon.png" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>OurTubes - Delete Channel</title>
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
    <li><a class="black-text center-align active" href="deleteChan">Delete</a></li>
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
    <div class="row">"""
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('getChans')
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    i = 0
    ret += """<ul class="col s6 push-s6  collection">"""
    if data and len(data) is not 0:
        for chan in data:
            if i == 0:
                ret += """<li class="collection-item">
                <p class="center-align"><b><i>Existing channels:</i></b></p></li>"""
            ret += """<li class="collection-item">
                <span>&#187;  """ + chan[1] + """</span></li>"""
            i += 1
    ret += """</ul>
    <div class="col s6 pull-s6 container jumbotron">
      <form class="form-signin">
        <label for="inputChanName" class="sr-only">Chan name</label>
        <input type="text" name="inputChanName" id="inputChanName" class="form-control" placeholder="Chan name" required autofocus>
        <label for="inputPrivatePassword" class="sr-only">Private Password</label>
        <input type="password" name="inputPrivatePassword" id="inputPrivatePassword" class="form-control" placeholder="Password" required>
        <button id="btnDelete" class="btn btn-lg btn-primary btn-block" type="button">Delete</button>
        <script>
          $(function() {
          $('#btnDelete').click(function() {
          $.ajax({
          url: '/delete',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
          Materialize.toast('Chan deleted', 3000, 'green')
          function show_popup(){
          location.reload();
          };
          window.setTimeout( show_popup, 3000 );
          },
          error: function(error) {
          Materialize.toast('Chan cannot be deleted', 4000, 'red')
          }
          });
          });
          });
        </script>
      </form>
    </div>
    </div>
    <footer class="page-footer red accent-5>
    <div class="footer-copyright">
    <p class="center">&copy; BunnyCompany 2018</p>
    </div>
    </footer>
    </body>
    </html>"""
    return ret
