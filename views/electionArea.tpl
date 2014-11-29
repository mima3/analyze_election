<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
  <title>小選挙区の区割り</title>
  <link rel="stylesheet" href="/analyze_election/js/select2/select2.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/js/jquery/jquery-ui.min.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/base.css" type="text/css" />
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-ui-1.10.4.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/select2/select2.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/blockui/jquery.blockUI.js"></script>
  <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
  <script type="text/javascript" src="/analyze_election/js/util.js"></script>
  <script type="text/javascript" src="/analyze_election/js/electionArea.js"></script>
</head>
<body>
  <div id="contents">
    <h1>小選挙区の区割り</h1>
    <select id="selPrefecture">
      <option value = ""></option>
      %for prefecture in prefectures:
        <option value = "{{prefecture}}">{{prefecture}}</option>
      %end
    </select>
    <select id="selElectionArea"><option>　　　　　　　　　　</option></select>
    <div id="map_canvas" style="width: 100%; height: 400px"></div>
    <table class="normal">
      <thead>
        <th>小区</th>
        <th>郡</th>
        <th>町</th>
        <th>メモ</th>
      </thead>
      <tbody id="tableElectionArea">
      </tbody>
    </table>
    <p>このデータは以下から取得したものです</p>
    <p><a href="http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03.html">国土数値情報　行政区域データ</a></p>
    <p><a href="http://www.soumu.go.jp/senkyo/senkyo_s/news/senkyo/shu_kuwari/">総務省　衆議院小選挙区の区割りの改定等について</a></p>
  </div>
</body>
</html>
