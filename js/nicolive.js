$(function() {
  $(document).ready(function() {
    var nicoLiveId = $('#nicoLiveId').attr('nicoLiveId');
    console.log(nicoLiveId);
    var terms;

    $("#termsTable").jqGrid({
      data:terms,
      datatype:"local",
      colNames:["単語","出現数"],
      colModel:[
        {name:'text'},
        {name:'weight',align:'right',sorttype:'int'}
      ],
      height:'100%',
      width:'100%',
      multiselect: false,
      caption: 'コメント中の単語'
    });

    $("#timesTable").jqGrid({
      data:terms,
      datatype:"local",
      colNames:["分","コメント数"],
      colModel:[
        {name:'maxtime'},
        {name:'count',align:'right',sorttype:'int'}
      ],
      height:'100%',
      width:'100%',
      multiselect: false,
      caption: '開演からのコメント数'
    });

    $("#usersTable").jqGrid({
      data:terms,
      datatype:"local",
      colNames:["ユーザID","コメント数"],
      colModel:[
        {name:'text'},
        {name:'weight',align:'right',sorttype:'int'}
      ],
      height:'100%',
      width:'100%',
      multiselect: false,
      caption: 'ユーザ毎のコメント数'
    });

    // コメント中の単語の出現数を取得
    util.getJson(
      '/analyze_election/niconico/term_' + nicoLiveId + '.json',
      {},
      function (errCode, result) {
        if (errCode) {
          return;
        }
        $('#termTagCloud').jQCloud(result);
        $('#termsTable').addRowData('1' , result);
      },
      function() {
        //$.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
      },
      function() {
        //$.unblockUI();
      }
    );

    // 時間別のコメント数
    util.getJson(
      '/analyze_election/niconico/vpos_' + nicoLiveId + '.json',
      {},
      function (errCode, result) {

        var list = [];
        for (var i = 0; i < result.length; ++i) {
          list.push([(result[i].maxtime / (100 * 60)) , result[i].count]);
          result[i].maxtime = (result[i].maxtime / (100 * 60));
        }

        $('#timesTable').addRowData('1' , result);

        $.jqplot(
            'timePlot',
            [
               list
            ],
            {
                seriesDefaults: {
                    renderer: $.jqplot.BarRenderer,
                },
                axes: {
                    xaxis: {
                        renderer: $.jqplot.CategoryAxisRenderer,
                    }
                }
            }
        );
      },
      function() {
        //$.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
      },
      function() {
        //$.unblockUI();
      }
    );

    // ユーザー別のコメント数
    util.getJson(
      '/analyze_election/niconico/user_' + nicoLiveId + '.json',
      {},
      function (errCode, result) {
        if (errCode) {
          return;
        }
        $('#usersTable').addRowData('1' , result);
      },
      function() {
        //$.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
      },
      function() {
        //$.unblockUI();
      }
    );

    jQuery('#commentTable').jqGrid({
      url: '/analyze_election/json/get_nicolive_comment/' + nicoLiveId,
      datatype: 'json',
      search: {
        groupOps: [{ op: 'AND'}]
      },
      colNames: ['user_id', 'premium', 'content', 'vpos', 'score', 'mail'],
      colModel: [
        {
          name: 'user_id',
          search: true,
          sortable: false,
          width: 100,
          searchoptions: {
            sopt: ['eq']
          }
        },{
          name: 'premium',
          search: true,
          sortable: false,
          width: 30,
          searchoptions: {
            sopt: ['eq']
          }
        },{
          name: 'content',
          search: true,
          sortable: false,
          width: 200,
          searchoptions: {
            sopt: ['in']
          }
        },{
          name: 'vpos',
          sortable: false,
          search: false,
          width: 60
        },{
          name: 'score',
          search: true,
          sortable: false,
          width: 60,
          searchoptions: {
            sopt: ['lt']
          }
        },{
          name: 'mail',
          search: true,
          sortable: false,
          width: 60,
          searchoptions: {
            sopt: ['eq']
          }
        }
      ],
      multiselect: false,
      height: '100%',
      caption: 'コメント',
      pager: '#commentPager'
    });
    jQuery('#commentTable').jqGrid(
      'navGrid',
      '#commentPager',
      {del: false, add: false, edit: false},
      {},
      {},
      {},
      {
        multipleSearch: true,
        beforeShowSearch: function($form) {
          //http://stackoverflow.com/questions/6116402/remove-search-operator-and-or-in-multiplesearch-jqgrid
          var searchDialog = $form[0];
          if (!searchDialog) return true;
          var oldrReDraw = searchDialog.reDraw; // save the original reDraw method
          var doWhatWeNeed = function() {
            // hide the AND/OR operation selection
            $('select.opsel', searchDialog).hide();

            setTimeout(function() {
              // set fucus in the last input field
              $('input[type="text"]:last', searchDialog).focus();
            }, 50);
          };
          searchDialog.reDraw = function() {
              oldrReDraw.call(searchDialog);    // call the original reDraw method
              doWhatWeNeed();
          };
          doWhatWeNeed();
          return true;
        }
      }
    ).jqGrid('gridResize');

  });
});