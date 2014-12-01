<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
  <title>ニコ生({{nicoliveId}})の解析</title>
  <link rel="stylesheet" href="/analyze_election/js/jsGrid/ui.jqgrid.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/select2/select2.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/jqcloud/jqcloud.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/jqplot/jquery.jqplot.min.css" type="text/css"/>
  <link rel="stylesheet" href="/analyze_election/js/jquery/jquery-ui.min.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/jquery/jquery.ui.theme.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/base.css" type="text/css" />
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-ui-1.10.4.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/select2/select2.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/blockui/jquery.blockUI.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jsGrid/jquery.jqGrid.src.js" ></script>
  <script type="text/javascript" src="/analyze_election/js/jsGrid/i18n/grid.locale-ja.js" ></script>
  <script type="text/javascript" src="/analyze_election/js/util.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jqcloud/jqcloud-1.0.4.min.js" ></script>
  <script type="text/javascript" src="/analyze_election/js/jqplot/jquery.jqplot.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jqplot/plugins/jqplot.barRenderer.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jqplot/plugins/jqplot.categoryAxisRenderer.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/nicolive.js"></script>
</head>
<body>
  <div id="contents">
    <h1>ニコ生(<a href="http://live.nicovideo.jp/watch/{{nicoliveId}}">{{nicoliveId}}</a>)の解析</h1>
    <h2>メニュー</h2>
    <ul>
      <li><a href="#termHead">コメント中の単語</a></li>
      <li><a href="#timeHead">開演からのコメント数</a></li>
      <li><a href="#userHead">発言者</a></li>
      <li><a href="#commentHead">全コメント</a></li>
    </ul>
    <h2 id="termHead">コメント中の単語</h2>
    <p>全コメント中に複数回、出現した単語数を集計します。</p>
    <div id="termTagCloud" style="width: 100%; height: 480px;"></div>
    <table id="termsTable" ></table>
    <h2 id="timeHead">開演からのコメント数</h2>
    <p>開演時間からのコメント数の遷移を表します。※放映開始時間ではありません</p>
    <div id="timePlot" style="width: 100%; height: 480px;"></div>
    <table id="timesTable" ></table>
    <h2 id="userHead">発言者</h2>
    <p>複数回コメントしたユーザの一覧を表示します。</p>
    <table id="usersTable" ></table>
    <h2 id="commentHead">全コメント</h2>
    <table id="commentTable" class="scroll"></table>
    <div id="commentPager" ></div>

  </div>
  <div id="nicoLiveId" nicoLiveId="{{nicoliveId}}"></div>
</body>
</html>
