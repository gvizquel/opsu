﻿/*
 Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
*/
(function(){CKEDITOR.plugins.add("ajax",{requires:"xml"});CKEDITOR.ajax=function(){function g(){if(!CKEDITOR.env.ie||"file:"!=location.protocol)try{return new XMLHttpRequest}catch(a){}try{return new ActiveXObject("Msxml2.XMLHTTP")}catch(b){}try{return new ActiveXObject("Microsoft.XMLHTTP")}catch(f){}return null}function h(a){return 4==a.readyState&&(200<=a.status&&300>a.status||304==a.status||0===a.status||1223==a.status)}function k(a){return h(a)?a.responseText:null}function m(a){if(h(a)){var b=
a.responseXML;return new CKEDITOR.xml(b&&b.firstChild?b:a.responseText)}return null}function l(a,b,f){var d=!!b,c=g();if(!c)return null;c.open("GET",a,d);d&&(c.onreadystatechange=function(){4==c.readyState&&(b(f(c)),c=null)});c.send(null);return d?"":f(c)}function n(a,b,f,d,c){var e=g();if(!e)return null;e.open("POST",a,!0);e.onreadystatechange=function(){4==e.readyState&&(d&&d(c(e)),e=null)};e.setRequestHeader("Content-type",f||"application/x-www-form-urlencoded; charset\x3dUTF-8");e.send(b)}return{load:function(a,
b){return l(a,b,k)},post:function(a,b,f,d){return n(a,b,f,d,k)},loadXml:function(a,b){return l(a,b,m)}}}()})();
