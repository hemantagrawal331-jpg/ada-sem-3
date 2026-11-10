var names = {
  car: "Car",
  bike: "Bike",
  ev: "EV",
  normal: "Normal",
  disabled: "Disabled",
  premium: "Premium"
};

function esc(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function nice(word) {
  if (names[word]) {
    return names[word];
  }
  return word;
}

function setMessage(text, ok) {
  var el = document.getElementById("message");
  el.textContent = text;
  if (ok) {
    el.style.color = "#1d6b32";
  } else {
    el.style.color = "#9d2c2c";
  }
}

function hideCompared() {
  var box = document.getElementById("comparePanel");
  box.className = "panel bottom hidden";
  box.innerHTML = "";
}

function drawCompared(rows, pickedId, score) {
  var html = "";
  html += "<h2>Scores put in the min heap</h2>";
  html += "<p class=\"note\">Lowest score was " + score + ", so " + esc(pickedId) + " was picked.</p>";
  html += "<table>";
  html += "<tr><th>Slot</th><th>Type</th><th>Distance</th><th>Score</th></tr>";

  for (var i = 0; i < rows.length; i++) {
    var r = rows[i];
    var cls = "";
    if (r.id === pickedId) {
      cls = " class=\"picked\"";
    }
    html += "<tr" + cls + ">";
    html += "<td>" + esc(r.id) + "</td>";
    html += "<td>" + esc(nice(r.type)) + "</td>";
    html += "<td>" + r.distance + "</td>";
    html += "<td>" + r.score + "</td>";
    html += "</tr>";
  }

  html += "</table>";
  var box = document.getElementById("comparePanel");
  box.className = "panel bottom";
  box.innerHTML = html;
}

function drawGrid(slots) {
  var html = "";
  var free = 0;

  for (var i = 0; i < slots.length; i++) {
    var s = slots[i];
    var cls = "slot";
    var statusHtml = "";

    if (s.status === "free") {
      free = free + 1;
      statusHtml = "<div class=\"st free\">FREE</div>";
    } else {
      cls = "slot occupied";
      statusHtml = "<div class=\"st busy\">OCCUPIED</div>";
      statusHtml += "<div class=\"vno\">" + esc(s.vehicle.number) + "</div>";
    }

    html += "<div class=\"" + cls + "\">";
    html += "<div class=\"sid\">" + esc(s.id) + "</div>";
    html += "<div class=\"meta\">" + esc(nice(s.type)) + " · dist " + s.distance + "</div>";
    html += statusHtml;
    html += "</div>";
  }

  document.getElementById("grid").innerHTML = html;
  document.getElementById("counts").textContent =
    "Free: " + free + "    Occupied: " + (slots.length - free);
}

function drawSorted(slots) {
  var html = "";

  for (var i = 0; i < slots.length; i++) {
    var s = slots[i];
    var who = "-";
    var statusText = "Free";
    if (s.vehicle) {
      who = s.vehicle.number;
      statusText = "Occupied";
    }
    html += "<tr>";
    html += "<td>" + esc(s.id) + "</td>";
    html += "<td>" + esc(nice(s.type)) + "</td>";
    html += "<td>" + s.distance + "</td>";
    html += "<td>" + statusText + "</td>";
    html += "<td>" + esc(who) + "</td>";
    html += "</tr>";
  }

  document.getElementById("sortedBody").innerHTML = html;
}

function drawParked(list) {
  var html = "";

  if (list.length === 0) {
    html = "<tr><td colspan=\"4\">No vehicles parked</td></tr>";
  } else {
    for (var i = 0; i < list.length; i++) {
      var p = list[i];
      html += "<tr>";
      html += "<td>" + esc(p.number) + "</td>";
      html += "<td>" + esc(p.slot_id) + "</td>";
      html += "<td>" + esc(nice(p.type)) + "</td>";
      html += "<td>" + esc(nice(p.priority)) + "</td>";
      html += "</tr>";
    }
  }

  document.getElementById("parkedBody").innerHTML = html;
}

function loadSlots() {
  fetch("/slots")
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      drawGrid(data.slots);
      drawSorted(data.by_distance);
      drawParked(data.parked);
    })
    .catch(function () {
      setMessage("Could not load the parking lot", false);
    });
}

function postJson(url, body) {
  return fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  }).then(function (res) {
    return res.json();
  });
}

document.getElementById("entryForm").addEventListener("submit", function (e) {
  e.preventDefault();
  var number = document.getElementById("vehicleNumber").value;
  var vtype = document.getElementById("vehicleType").value;
  var priority = document.getElementById("priority").value;

  postJson("/allocate", { number: number, type: vtype, priority: priority })
    .then(function (data) {
      setMessage(data.message, data.ok);
      if (data.ok) {
        document.getElementById("vehicleNumber").value = "";
        drawCompared(data.compared, data.slot_id, data.score);
      } else {
        hideCompared();
      }
      loadSlots();
    })
    .catch(function () {
      setMessage("Could not allocate", false);
    });
});

document.getElementById("exitForm").addEventListener("submit", function (e) {
  e.preventDefault();
  var number = document.getElementById("exitNumber").value;

  postJson("/release", { number: number })
    .then(function (data) {
      setMessage(data.message, data.ok);
      if (data.ok) {
        document.getElementById("exitNumber").value = "";
        hideCompared();
      }
      loadSlots();
    })
    .catch(function () {
      setMessage("Could not free the slot", false);
    });
});

document.getElementById("findForm").addEventListener("submit", function (e) {
  e.preventDefault();
  var number = document.getElementById("findNumber").value;

  postJson("/find", { number: number })
    .then(function (data) {
      setMessage(data.message, data.ok);
    })
    .catch(function () {
      setMessage("Could not find the vehicle", false);
    });
});

loadSlots();
