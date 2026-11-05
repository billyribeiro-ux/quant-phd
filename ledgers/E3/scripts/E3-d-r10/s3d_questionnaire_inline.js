
        (function () {
          const root = document.querySelector("[data-questionnaire]");
          if (!root) return;
          root.replaceChildren();
          const statusLine = document.createElement("p");
          statusLine.setAttribute("role", "status");
          const fileInput = document.createElement("input");
          fileInput.type = "file";
          fileInput.accept = "application/json,.json";
          fileInput.id = "q-file";
          const fileLabel = document.createElement("label");
          fileLabel.htmlFor = "q-file";
          fileLabel.textContent = "Instrument file (instrument.json) ";
          const pairList = document.createElement("ol");
          const exportButton = document.createElement("button");
          exportButton.type = "button";
          exportButton.className = "button";
          exportButton.textContent = "Export responses.json";
          exportButton.disabled = true;
          fileLabel.append(fileInput);
          root.append(fileLabel, statusLine, pairList, exportButton);
          let pairs = [];

          const isProbability = (text) => typeof text === "string" && /^(0|1|\d+\/\d*[1-9]\d*)$/.test(text);
          const isLottery = (prizes, probs) =>
            Array.isArray(prizes) && Array.isArray(probs) && prizes.length > 0 && prizes.length === probs.length &&
            prizes.every(Number.isInteger) && probs.every(isProbability);
          const describe = (prizes, probs) => prizes.map((x, i) => x + " cents with probability " + probs[i]).join("; ");

          fileInput.addEventListener("change", async () => {
            pairList.replaceChildren();
            exportButton.disabled = true;
            pairs = [];
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;
            try {
              const data = JSON.parse(await file.text());
              if (!Array.isArray(data) || data.length === 0) {
                throw new Error("the file must be a non-empty JSON list of pairs");
              }
              data.forEach((p, i) => {
                if (!p || typeof p !== "object" || !Number.isInteger(p.pair_id) ||
                    !isLottery(p.prizes_a, p.probs_a) || !isLottery(p.prizes_b, p.probs_b)) {
                  throw new Error("entry " + i + " lacks a whole-number pair_id, or a lottery with whole cents and probabilities written as numerator/denominator or as whole numbers");
                }
              });
              pairs = data;
              pairs.forEach((p, i) => {
                const fieldset = document.createElement("fieldset");
                fieldset.style.minInlineSize = "0";
                const legend = document.createElement("legend");
                legend.textContent = "Pair " + p.pair_id + ". A: " + describe(p.prizes_a, p.probs_a) +
                  ". B: " + describe(p.prizes_b, p.probs_b) + ".";
                fieldset.append(legend);
                for (const choice of ["A", "B"]) {
                  const option = document.createElement("label");
                  const radio = document.createElement("input");
                  radio.type = "radio";
                  radio.name = "q-pair-" + i;
                  radio.value = choice;
                  option.append(radio, " " + choice + " ");
                  fieldset.append(option);
                }
                const item = document.createElement("li");
                item.append(fieldset);
                pairList.append(item);
              });
              statusLine.textContent = pairs.length + " pairs loaded. Record one choice for each pair, then export.";
              exportButton.disabled = false;
            } catch (err) {
              statusLine.textContent = "The file was not loaded: " + err.message + ".";
            }
          });

          exportButton.addEventListener("click", () => {
            const responses = [];
            const missing = [];
            pairs.forEach((p, i) => {
              const chosen = pairList.querySelector('input[name="q-pair-' + i + '"]:checked');
              if (!chosen) {
                missing.push(p.pair_id);
                return;
              }
              responses.push({
                pair_id: p.pair_id, choice: chosen.value,
                prizes_a: p.prizes_a, probs_a: p.probs_a, prizes_b: p.prizes_b, probs_b: p.probs_b
              });
            });
            if (missing.length > 0) {
              const several = missing.length > 1;
              statusLine.textContent = "No export: " + (several ? "pairs " : "pair ") + missing.join(", ") +
                (several ? " have" : " has") + " no choice yet.";
              return;
            }
            const url = URL.createObjectURL(new Blob([JSON.stringify(responses, null, 2)], { type: "application/json" }));
            const link = document.createElement("a");
            link.href = url;
            link.download = "responses.json";
            document.body.append(link);
            link.click();
            link.remove();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
            statusLine.textContent = "Exported " + responses.length + " responses to responses.json.";
          });
        })();
        