# LX1 open items

Open items for unit LX1 (Financial History). Each item is a request to the architect; no shared file was edited.

## Data request

- **D-1 (L03 curriculum lab).** Source URL, series ID, licence and transform: not identified. The curriculum names embedded data for the L03 lab (`curriculum/06-profession-capstone.yaml:41`), but no redistributable historical series for gold-standard adherence or output depth is in `tools/data_sources.yaml`, and none has been read. Until a source is admitted with its redistribution grant quoted from the issuer's page, `lab-LX1-L03-1` stays SIMULATED, and L03 states its honest-pending note. Needed for: the L03 lab, if the architect wants real historical data.

## Definitions waiting for a source

- **Bretton Woods system (L04).** The historical definition and any date for the system's end wait for a primary or survey source from an allow-listed issuer or a publisher's stable URL. Until then, L04 carries the concept as a pending definition (`def-bretton-woods-system`), and the page defines only its fixed-parity model.
- **Architect decision needed.** `tools/check_dag.py` requires every concept the curriculum assigns to LX1 to be defined with a `<dfn>` on the unit's pages. The pending definition satisfies that check without stating a historical fact. The architect should confirm this reading, or record a different one in the build plan.

## Reference requests

- **Credit-channel attribution (L03, B2).** The curriculum source string is Bernanke (1983), AER 73(3) (`curriculum/06-profession-capstone.yaml:38`). The registry has no record for it. The review-queue candidate (DOI 10.3386/w1054) is an NBER working paper and must not be admitted as the AER article. No empirical credit-channel claim is made until a correct record is admitted.
- **Kindleberger and Aliber (L01, N1).** The curriculum source string is at `curriculum/06-profession-capstone.yaml:36`. The review-queue candidate lists a different first author and is not admitted.
- **Friedman and Schwartz record (N2).** The registry record `friedman1963monetary` lists Friedman only. Pages cite the key and do not type the second author. The architect may correct the record through `tools/add_reference.py`.
