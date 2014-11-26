$(function() {
  $(document).ready(function() {
    var pt = new google.maps.LatLng(41.925926, 143.240137);
    var mapOptions = {
      center: pt,
      zoom: 7
    };
    var map = new google.maps.Map(
      document.getElementById('map_canvas'),
      mapOptions
    );
    var polylines=[];
    var geocoder = new google.maps.Geocoder();

    $('#selPrefecture').select2({
      width: 'resolve' ,
      dropdownAutoWidth: true
    });
    $('#selPrefecture').select2('val', '');

    $('#selElectionArea').select2({
      width: 'resolve' ,
      dropdownAutoWidth: true
    });

    $('#selPrefecture').change(function() {
      var prefecture = $('#selPrefecture').val();
      console.log(prefecture);
      if (!prefecture) {
        return;
      }
      $('#selElectionArea').select2('val', '');
      $('#selElectionArea').empty();

      util.getJson(
        '/analyze_election/json/get_prefecture_election_area',
        {
          prefectureName: prefecture
        },
        function (errCode, result) {
          console.log(errCode);
          console.log(result);
          if (errCode) {
            return;
          }
          for (var i = 0; i < result.length; ++i) {
            var opt = $('<option>').html(result[i]).val(result[i]);
            $('#selElectionArea').append(opt);
          }
        },
        function() {
          $.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
        },
        function() {
          $.unblockUI();
        }
      );
    }).keyup(function() {
      $(this).blur().focus();
    });

    $('#selElectionArea').change(function() {
      var electionArea = $('#selElectionArea').val();
      console.log(electionArea);
      if (!electionArea) {
        return;
      }
      util.getJson(
        '/analyze_election/json/get_election_area_information',
        {
          electionArea: electionArea
        },
        function (errCode, result) {
          if (errCode) {
            return;
          }
          for(var i = 0; i < polylines.length; ++i) {
            polylines[i].setMap(null);
          }
          polylines = [];
          var tbl = $('#tableElectionArea');
          tbl.empty();
          for (var i = 0; i < result.length; ++i ) {
            console.log(result[i]);
            var tr = $('<tr/>');
            $('<td>' + result[i].subPrefectureName + '</td>').appendTo(tr);
            $('<td>' + result[i].countyName + '</td>').appendTo(tr);
            $('<td>' + result[i].cityName + '</td>').appendTo(tr);
            $('<td>' + result[i].notes + '</td>').appendTo(tr);
            tr.appendTo(tbl);

            var data = result[i].geo;
            for (var id in data) {
              var points = [];
              for (var j = 0; j < data[id].length; ++j) {
                 if (i == 0 && j== 0 && polylines.length==0) {
                   map.panTo(new google.maps.LatLng(data[id][j][0],data[id][j][1]));
                 }
                 points.push(new google.maps.LatLng(data[id][j][0],data[id][j][1]));
              }
              var poly = new google.maps.Polyline({
                path: points,
                strokeColor: "#00FF00",
                strokeOpacity: 1.0,
                strokeWeight: 2
              });
              poly.setMap(map);
              polylines.push(poly);
            }
          }
          
        },
        function() {
          $.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
        },
        function() {
          $.unblockUI();
        }
      );
    }).keyup(function() {
      $(this).blur().focus();
    });
  });
});