<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
  <title>{{year}}年の各政党のホームページ解析</title>
  <link rel="stylesheet" href="/analyze_election/js/jqcloud/jqcloud.css" type="text/css" />
  <link rel="stylesheet" href="/analyze_election/base.css" type="text/css" />
  <script type="text/javascript" src="/analyze_election/js/jquery/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="/analyze_election/js/jqcloud/jqcloud-1.0.4.min.js" ></script>
  <script type="text/javascript" src="/analyze_election/js/analyzehp.js" ></script>
</head>
<body>
  <div id="contents">
    <h1>{{year}}年の各政党のホームページ解析</h1>
    <h2>概要</h2>
    <p>このページは各政党のホームページから単語を抽出して、tr-idfを取得して、各政党間の距離を取得します.</p>
    <p>歴史のある政党に関しては、今回の選挙の特徴が出やすいように、解析対象のホームページの数を絞っています。</p>
    <h3>tf-idfによる文章の解析</h3>
    <p>文章ｙにおいて単語ｘのtf-idfの値は以下のようになる。</p>
    <p>tf = 文章y中に単語xが登場した数 / 文章中の単語数</p>
    <p>idf = 1.0 + log( 文章の総数 / 単語xが登場する文章の数 )</p>
    <p>tf-idf = tf × idf</p>
    <p>多くのドキュメントに登場する単語は重要度が下がりスコアが低くなり、特定のドキュメントにしか登場しない単語は重要度があがりスコアが大きくなる</p>
    <h3>コサイン類似度による文章の距離の測定</h3>
    <p>文章1が単語(A,B,C)を持っており、その単語のTF-IDFの値が(0.1,0.2,0.3)とする。</p>
    <p>文章2が単語(C,D,E)をもっており、その単語のTF-IDFの値が(0,4,0.5,0.6)とする。</p>
    <p>文章に存在しない単語のTF-IDFを０とするとして、全ての単語についてのTF-IDFを作成する。</p>
    <p>文章1の(A,B,C,D,E)は(0.1,0.2,0.3,0,0)となる。</p>
    <p>文章2の(A,B,C,D,E)は(0,0,0.4,0.5,0.6)となる</p>
    <p>この文章1と文章２のベクトルの角度のコサインは両者の類似度を表す。</p>
    <p>まったく同じ文章の場合は文章１と文章２の角度は0度になる。</p>

    <h2>各政党のtf-idfの距離</h2>
    <img src="/analyze_election/script_comp_manifesto/party_hp_result_2014.png" width="100%"></img>
    <h2>各政党の情報</h2>
    %for party in party_result_data:
        <h3 id="{{party['name']}}">{{party['name']}}</h2>
        <p>取得期間：{{party['info']['min']}} ～ {{party['info']['max']}}</p>
        <p>取得ページ：{{party['info']['count']}} 件</p>
        %for p in party_data:
            %if p['name'] == party['name']:
               <p>取得開始のURL：<a href="{{p['root_url']}}">{{p['root_url']}}</a></p>
               <p>有効なURLの開始文字列:
               %for s in p['positive_list']:
               「{{s}}」
               %end
               </p>
               <p>無効なURLの開始文字列:
               %for s in p['exclude_filter']:
               「{{s}}」
               %end
               </p>
            %end
        %end
        <div class="words" name="{{party['name']}}">
          <div class="tagcloud" style="width: 100%; height: 480px;"></div>
          <p>上位100件の単語:</p>
          <table class="normal">
              <tr>
                <th>単語</th>
                <th>tf-idf</th>
              </tr>
              %for w in party['words']:
              <tr class="data" text="{{w['text']}}" weight="{{w['weight']}}">
                 <td>{{w['text']}}</td>
                 <td>{{w['weight']}}</td>
              </tr>
              %end
          </table>
        </div>
    %end
</body>
</html>
