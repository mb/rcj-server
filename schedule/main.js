window.onload = function () {
  fetch("/schedule/runs")
    .then((response) => response.json())
    .then((json) => {
      displaySchedule(json);
    })
    .catch((error) => {
      console.log(error);
    });
};

function displaySchedule(scheduledRuns) {
  scheduledRuns = scheduledRuns
    .map((run) => createRequiredTimeFormatsForRun(run))
    .sort((a, b) => {
      const timeDiff = a._time.unixTime - b._time.unixTime;
      return timeDiff !== 0 ? timeDiff : a.runId - b.runId;
    });
  const runsGroupedByCompetitionDayArena = {
    // competition: { date: { arena: [] } }
    "line-entry": {},
    line: {},
  };
  for (const run of scheduledRuns) {
    if (!(run.competition in runsGroupedByCompetitionDayArena)) runsGroupedByCompetitionDayArena[run.competition] = {};
    if (!(run._time.isoDateString in runsGroupedByCompetitionDayArena[run.competition]))
      runsGroupedByCompetitionDayArena[run.competition][run._time.isoDateString] = {};
    if (!(run.arenaId in runsGroupedByCompetitionDayArena[run.competition][run._time.isoDateString]))
      runsGroupedByCompetitionDayArena[run.competition][run._time.isoDateString][run.arenaId] = [];
    runsGroupedByCompetitionDayArena[run.competition][run._time.isoDateString][run.arenaId].push(run);
  }

  for (const competition of Object.keys(runsGroupedByCompetitionDayArena)) {
    for (const day of Object.keys(runsGroupedByCompetitionDayArena[competition])) {
      const container = document.getElementById(`container-${competition}-${day}`);
      if (!container) {
        console.log("No container for", { competition, day });
        continue;
      }
      const arenaIds = Object.keys(runsGroupedByCompetitionDayArena[competition][day]).sort();

      const title = document.createElement("span");
      title.textContent = { "line-entry": "Rescue Line Entry", line: "Rescue Line" }[competition] + " " + day;
      container.appendChild(title);

      const table = document.createElement("table");
      const headerRow = document.createElement("tr");
      headerRow.appendChild(document.createElement("td"));
      for (const arenaId of arenaIds) {
        const headerCell = document.createElement("td");
        headerCell.textContent = `Arena ${arenaId}`;
        headerRow.appendChild(headerCell);
      }
      table.appendChild(headerRow);
      container.appendChild(table);

      const firstRunTime = Math.min(
        ...arenaIds.map((arenaId) => runsGroupedByCompetitionDayArena[competition][day][arenaId][0]._time.unixTime)
      );
      const lastRunTime = Math.max(
        ...arenaIds.map(
          (arenaId) =>
            runsGroupedByCompetitionDayArena[competition][day][arenaId][
              runsGroupedByCompetitionDayArena[competition][day][arenaId].length - 1
            ]._time.unixTime
        )
      );
      const slotLengthInMinutes = 10; // TODO: find next run and get difference
      const tableCells = [];
      let currentTime = firstRunTime;
      while (true) {
        if (currentTime > lastRunTime) break;
        const row = [];
        row.push(getTextForTimeCell(currentTime, slotLengthInMinutes));
        for (let i = 0; i < arenaIds.length; i++) {
          row.push(undefined);
        }
        tableCells.push(row);
        currentTime += slotLengthInMinutes * 60;
      }
      let arenaIndex = 0;
      for (const arenaId of arenaIds) {
        for (const run of runsGroupedByCompetitionDayArena[competition][day][arenaId]) {
          const slot = Math.floor((run._time.unixTime - firstRunTime) / (slotLengthInMinutes * 60));
          tableCells[slot][arenaIndex + 1] = run.teamId;
        }
        arenaIndex++;
      }

      for (const row of tableCells) {
        const tr = document.createElement("tr");
        for (const cellContent of row) {
          const td = document.createElement("td");
          td.textContent = cellContent || "-";
          tr.appendChild(td);
        }
        table.appendChild(tr);
      }
    }
  }
}

function createRequiredTimeFormatsForRun(run) {
  // run.time is a ISO 8601 string, e.g. "2022-04-01T12:34:56+02"
  const date = new Date(run.time + (run.time.match(/(\+|-)\d\d$/) ? "00" : ""));
  run._time = {
    date,
    unixTime: Math.floor(date.getTime() / 1000),
    isoDateString: run.time.split("T")[0],
  };
  return run;
}

function getTextForTimeCell(unixtime, slotLengthInMinutes) {
  const start = new Date(unixtime * 1000);
  const end = new Date((unixtime + slotLengthInMinutes * 60) * 1000);
  return `${formatDate(start, "HH:mm")} - ${formatDate(end, "HH:mm")}`;
}

function formatDate(date, formatStr) {
  return formatStr
    .replace("YYYY", pad(date.getFullYear(), 4))
    .replace("MM", pad(date.getMonth() + 1, 2))
    .replace("DD", pad(date.getDate(), 2))
    .replace("HH", pad(date.getHours(), 2))
    .replace("mm", pad(date.getMinutes(), 2))
    .replace("ss", pad(date.getSeconds(), 2));
}

function pad(text, length, padChar = "0", padFront = true) {
  text = String(text);
  const padChars = padChar.repeat(length - text.length).substr(0, length - text.length);
  return padFront ? padChars + text : text + padChars;
}
