$(function() {
  var lCurEditRow;
  var lCurEditCol;
  function calc_dondt(successFunc)
  {
    var max_seats = $("#max_seats").val();
    $("#votes").restoreCell(lCurEditRow,lCurEditCol);
    var vote_data = $("#votes").getRowData();
    $.ajax({
      type:'POST',
      url: 'main.py?CalcDondt',
      data: { max_seats:max_seats,vote_data:JSON.stringify(vote_data)},
      dataType:'json',
      success: function(json) {
        vote_data=json;
        $("#votes").clearGridData();
        $("#votes").addRowData("1",vote_data);
      },
      complete:function(json) {
      },
      error: function(xhr, textStatus, errorThrown){
        alert('Failed CalcDondt.' );
      }
    });
  }

  $(document).ready(function()
  {
    var vote_data = [
      {
        name: '自民党',
        votes: 0,
        max: 0,
        seats: 0
      }
    ];
    $("#calc_dondt").button().click(function(event){
      event.preventDefault();
      calc_dondt( function() {} );
    });
    $("#votes").jqGrid({
      data:vote_data,
      datatype:"local",
      colNames:["政党","立候補者数","投票数","議席"],
      colModel:[
        {name:'name'},
        {name:'max', editable:true,edittype:'text',align:'right',editrules:{integer:true}, formatter:'integer',sorttype:'int'},
        {name:'votes', editable:true,edittype:'text',align:'right',editrules:{integer:true}, formatter:'integer',sorttype:'int'},
        {name:'seats',align:'right',sorttype:'int'},
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
      cellEdit:true,
      cellsubmit:'clientArray',
    });
  });
});