﻿/*
 Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
*/
(function(){CKEDITOR.dialog.add("codeSnippet",function(c){var b=c._.codesnippet.langs,d=c.lang.codesnippet,g=document.documentElement.clientHeight,e=[],f;e.push([c.lang.common.notSet,""]);for(f in b)e.push([b[f],f]);b=CKEDITOR.document.getWindow().getViewPaneSize();c=Math.min(b.width-70,800);b=b.height/1.5;650>g&&(b=g-220);return{title:d.title,minHeight:200,resizable:CKEDITOR.DIALOG_RESIZE_NONE,contents:[{id:"info",elements:[{id:"lang",type:"select",label:d.language,items:e,setup:function(a){a.ready&&
a.data.lang&&this.setValue(a.data.lang);!CKEDITOR.env.gecko||a.data.lang&&a.ready||(this.getInputElement().$.selectedIndex=-1)},commit:function(a){a.setData("lang",this.getValue())}},{id:"code",type:"textarea",label:d.codeContents,setup:function(a){this.setValue(a.data.code)},commit:function(a){a.setData("code",this.getValue())},required:!0,validate:CKEDITOR.dialog.validate.notEmpty(d.emptySnippetError),inputStyle:"cursor:auto;width:"+c+"px;height:"+b+"px;tab-size:4;text-align:left;","class":"cke_source"}]}]}})})();
