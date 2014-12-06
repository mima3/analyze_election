$(function() {
  var lCurEditRow;
  var lCurEditCol;

  $(document).ready(function()
  {
    var electionId = $('#electionId').attr('electionId');
    var storedata = store.get('analyze_election');
    if (!storedata) {
      storedata = {}
      storedata['dondt'] = {};
      storedata['dondt'][electionId] = {};
    }
    $("#calc_dondt").button().click(function(event){
      $("#votes").restoreCell(lCurEditRow,lCurEditCol);
      var vote_data = $("#votes").getRowData();
      storedata['dondt'][electionId] = {};
      for (var i = 0; i < vote_data.length; ++i) {
        var key = vote_data[i].block + '_' + vote_data[i].party;
        storedata['dondt'][electionId][key] = vote_data[i].votes;
      }
      store.set('analyze_election', storedata);

      $.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
      $.ajax({
        type:'POST',
        url: '/analyze_election/json/calc_dondt/' + electionId,
        data: {vote_data: JSON.stringify(vote_data)},
        dataType:'json',
        success: function(json) {
          $("#votes").clearGridData();
          $("#votes").addRowData('1',json.vote_data);
          $('#votes').groupingGroupBy('block');

          $("#result").clearGridData();
          $("#result").addRowData('1',json.result);
        },
        complete:function(json) {
          $.unblockUI();
        },
        error: function(xhr, textStatus, errorThrown){
          alert('Failed CalcDondt.' );
          $.unblockUI();
        }
      });
    });

    $("#votes").jqGrid({
      data: undefined,
      datatype:"local",
      rowNum:1000,
      colNames:["ブロック","政党","立候補者数","投票数","議席"],
      colModel:[
        {name:'block',sortable: false, editable:false},
        {name:'party',sortable: false, editable:false},
        {name:'max', sortable: false,editable:false, align:'right', formatter:'integer'},
        {name:'votes',sortable: false, editable:true,edittype:'text',align:'right',editrules:{integer:true}, formatter:'integer'},
        {name:'seats',sortable: false, align:'right'},
      ],
      height:'100%',
      width:'100%',
      multiselect: false,
      caption: 'ドント式比例議席数',
      afterSaveCell: function(rowid, cellname,value,iRow,iCol){
      },
      beforeEditCell: function(rowid,cellname,value,iRow,iCol) {
        lCurEditRow = iRow;
        lCurEditCol = iCol;
        
      },
      grouping:true,
      groupingView : {
        groupField : ['block'],
        groupColumnShow : [false],
        groupText : ['<b>{0} - {1} Item(s)</b>']
      },
      cellEdit:true,
      cellsubmit:'clientArray',
    });

    util.getJson(
      '/analyze_election/json/dondt/' + electionId,
      {},
      function (errCode, result) {
          $("#votes").clearGridData();
          for (var i = 0; i < result.length; ++i) {
            var key = result[i].block + '_' + result[i].party;
            if (storedata['dondt'][electionId][key]) {
              result[i].votes = storedata['dondt'][electionId][key];
            }
          }
          $("#votes").addRowData("1",result);
          $('#votes').groupingGroupBy('block');
      },
      function() {
        $.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
      },
      function() {
        $.unblockUI();
      }
    );

    $("#result").jqGrid({
      data:undefined,
      datatype:"local",
      colNames:["党名","議席数"],
      colModel:[
        {name:'party'},
        {name:'seats',align:'right',sorttype:'int'}
      ],
      height:'100%',
      width:'100%',
      multiselect: false,
      caption: '計算数'
    });
  });

});