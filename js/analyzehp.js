$(function() {
  $(document).ready(function() {
    var words = $('.words');
    for(var i = 0; i < words.length; ++i) {
      var list = [];
      var name = words[i].attributes.name.nodeValue;
      var datas = $(words[i]).find('.data');
      for(var j = 0; j < datas.length; ++j) {
        list.push({
          text : datas[j].attributes.text.nodeValue,
          weight : datas[j].attributes.weight.nodeValue
        });
      }
      $(words[i]).find('.tagcloud').jQCloud(list);
    }
  });
});