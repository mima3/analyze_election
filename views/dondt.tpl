<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
  <title>ドント式の計算</title>
  <link rel="stylesheet" href="/analyze_election/js/jsGrid/ui.jqgrid.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/select2/select2.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/jquery/jquery-ui.min.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/base.css" type="text/css" />
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-ui-1.10.4.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/select2/select2.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/blockui/jquery.blockUI.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jsGrid/jquery.jqGrid.src.js" ></script>
  <script type="text/javascript" src="/analyze_election/js/jsGrid/i18n/grid.locale-ja.js" ></script>
  <script type="text/javascript" src="/analyze_election/js/util.js"></script>
  <script type="text/javascript" src="/analyze_election/js/dondt.js"></script>
</head>
<body>
  <div id="contents">
    <h1>ドント式の計算</h1>
    <table id="votes" ></table>
    <p>議席数 <input id="max_seats" name="max_seats"  size="50" value="48"/></p>
    <p><button id="calc_dondt">試算</button></p>
  </div>
</body>
</html>
