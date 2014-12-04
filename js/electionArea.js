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
    $('#getCurPos').button().click(function() {
      if (!navigator.geolocation) {
        //Geolocation APIを利用できない環境向けの処理
        alert('GeolocateAPIが使用できません');
      }
      navigator.geolocation.getCurrentPosition(function(position) {
        $('#selElectionArea').select2('val', '');
        $('#selElectionArea').empty();
        util.getJson(
          '/analyze_election/json/get_prefecture_election_area_by_pos',
          {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          },
          function (errCode, result) {
            if (errCode) {
              return;
            }
            updateSelElectionArea(result);
          },
          function() {
            $.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
          },
          function() {
            $.unblockUI();
          }
        );
      },function(positionError) {
        consloe.log(positionError.message);
      });
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
          if (errCode) {
            return;
          }
          updateSelElectionArea(result);
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

    // 小選挙区のエリア変更
    $('#selElectionArea').change(function() {
      var electionArea = $('#selElectionArea').val();
      console.log(electionArea);
      if (!electionArea) {
        return;
      }
      util.getJson(
        '/analyze_election/json/get_election_area_information',
        {
          electionArea: electionArea,
          electionId: $('#electionId').attr('electionId')
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
          area = result.area;
          for (var i = 0; i < area.length; ++i ) {
            var tr = $('<tr/>');
            $('<td>' + area[i].subPrefectureName + '</td>').appendTo(tr);
            $('<td>' + area[i].countyName + '</td>').appendTo(tr);
            $('<td>' + area[i].cityName + '</td>').appendTo(tr);
            $('<td>' + area[i].notes + '</td>').appendTo(tr);
            tr.appendTo(tbl);

            var data = area[i].geo;
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
          var tbl = $('#tableCandidate');
          tbl.empty();
          candidates = result.candidate;
          for (var i = 0; i < candidates.length; ++i ) {
            var tr = $('<tr/>');
            $('<td>' + candidates[i].name + '</td>').appendTo(tr);
            $('<td>' + candidates[i].age + '</td>').appendTo(tr);
            $('<td>' + candidates[i].party + '</td>').appendTo(tr);
            $('<td>' + candidates[i].status + '</td>').appendTo(tr);
            var net = createLink(candidates[i].twitter, 'twitter') + "<BR>" +
                      createLink(candidates[i].facebook, 'facebook') + "<BR>" +
                      createLink(candidates[i].homepage, 'homepage')
            $('<td>' + net + '</td>').appendTo(tr);
            tr.appendTo(tbl);
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
  function createLink(url, title) {
    if (!url) {
      return url;
    }
    return '<a href="' + url + '">' + title +'</a>';
  }
  function updateSelElectionArea(result) {
    var opt = $('<option>').html('').val(result[i]);
    $('#selElectionArea').append(opt);
    for (var i = 0; i < result.length; ++i) {
      var opt = $('<option>').html(result[i]).val(result[i]);
      $('#selElectionArea').append(opt);
    }
  }
});