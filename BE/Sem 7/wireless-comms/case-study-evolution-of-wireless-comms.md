# Case Study: Evolution of Network Communication Generations from 1G to 5G

**Subject:** Wireless Communication  
**Focus:** Cellular network generations — standards, air interface, core, and services (1G → 5G)  
**Sources:** Wikipedia (1G–5G, plus brief 6G outlook), plus two short side notes (G vs GHz; Akashvani).

---

## 1. Aim and scope

This case study follows **how public cellular networks changed generation by generation**: analog voice (1G) → digital voice and SMS (2G) → mobile internet (3G) → all-IP broadband (4G) → 5G New Radio and a service-based core.

**In scope:** radio access + core architecture, ITU/3GPP (and 3GPP2) standards, typical rates, launch milestones, and sunsets.

**Out of scope:** history of radio as a whole, Wi-Fi/Bluetooth, broadcast, spectrum theory except where a generation *uses* a band. Those are not the story.

**What “generation” means**

A new G is a **non-backward-compatible** step in the mobile *network*: new air interface and/or core, higher capacity, and a new service model (voice → SMS/data → mobile web → all-IP → eMBB / URLLC / mMTC). About **one G per decade**. ITU names the box (IMT-2000, IMT-Advanced, IMT-2020); 3GPP / 3GPP2 fill it.

> **Corner — “2G = 2 GHz”?** No. **G** = generation (GSM, LTE, NR). **GHz** = frequency. 5G often runs at **~3.5 GHz**, not 5 GHz.

> **Corner — Akashvani.** All India Radio (“voice from the sky”) is **broadcast**, 1930s onward — not a cellular G.

---

## 2. Comparative map

| Gen | Era | Air / switching | Headline standards | Service jump | Order-of-magnitude data |
| --- | --- | --- | --- | --- | --- |
| **1G** | late 1970s–80s | Analog FM; circuit | AMPS, NMT, TACS | Mobile voice | Voice only |
| **2G** | 1991– | Digital TDMA/CDMA; circuit + SMS | **GSM**, cdmaOne, D-AMPS | Encrypted voice, SMS; GPRS/EDGE later | GPRS ~40 kbit/s; EDGE ~384 kbit/s (theory) |
| **3G** | 2001– | Spread spectrum; CS + PS | **UMTS/W-CDMA**, CDMA2000; HSPA+ | Mobile internet, video | IMT-2000 ≥144 kbit/s; HSPA+ tens of Mbit/s |
| **4G** | 2009– | **All-IP**; OFDMA + MIMO | **LTE**, LTE-Advanced | HD streaming, VoLTE | IMT-Advanced: 100 Mbit/s mobile / 1 Gbit/s low mobility |
| **5G** | 2019– | 5G NR; NSA then SA 5GC | **5G NR**, IMT-2020 | eMBB, slicing, URLLC/mMTC path | IMT-2020 peaks 20/10 Gbit/s (ideal) |

---

## 3. 1G — Analog cellular

**1G** is the later name for analog public cellular. The real invention is the **cell**: low-power sites, **frequency reuse**, capacity from geography not just power.

**Milestones:** Bell Labs Chicago 1978 · **NTT Japan 1979** (first commercial) · **NMT** Sweden 1981 (roaming) · **AMPS** / Ameritech USA 1983, Motorola DynaTAC.

**Tech:** analog **FM** voice on the air; some digital signalling on the backbone. Regional, incompatible: AMPS, NMT, TACS, C-450, Radiocom 2000, RTMI, MCS/JTACS.

**Limits:** spectrum hungry, no voice encryption, no SMS/data as a first-class service. Most gone by early 2000s; last known commercial 1G (Russia) **2017**.

---

## 4. 2G — Digital voice, SMS, then packet add-ons

**Break from 1G:** the **radio hop is digital**.

**Launch:** **GSM**, Radiolinja, Finland, **1991** (ETSI). **cdmaOne (IS-95)** 1995. Also D-AMPS (N. America), PDC/PHS (Japan).

**Gains:** radio encryption · more users per MHz · **SMS**, then MMS, then packet.

| Step | Change | Rate (theory) |
| --- | --- | --- |
| GSM | Digital TDMA voice + SMS | Circuit data only |
| **GPRS** (2.5G) | Packet domain | ~40 kbit/s |
| **EDGE** (2.75G) | 8PSK | ~384 kbit/s (AT&T 2003) |
| Evolved EDGE | ~1 Mbit/s | Almost unused |

**Sunset:** 2G still used for IoT / feature phones. Some operators **kill 3G first** and keep 2G as fallback. GSM crypto is weak; OS settings can disable 2G.

---

## 5. 3G — IMT-2000, mobile internet

**ITU IMT-2000** is the 3G box. Usual floor **≥144 kbit/s**; products were faster.

| Family | Body | Radio | From |
| --- | --- | --- | --- |
| **UMTS** | **3GPP** | **W-CDMA** (TD-SCDMA in China) | GSM world |
| **CDMA2000** | **3GPP2** | 1x / **EV-DO** | IS-95 |

Both **spread spectrum**.

**Launches:** NTT DoCoMo **FOMA**, 1 Oct **2001** · SK Telecom EV-DO Korea Jan 2002 · Verizon 2002 · Hutchison “3” 2003 · India **MTNL** Delhi/Mumbai **11 Dec 2008**, then BSNL. Europe’s **3G auctions** (collectively **>$100B**) slowed some builds.

**HSPA / HSPA+:** tens of Mbit/s — USB dongles, early smartphones, “mobile broadband.” Mutual authentication; **KASUMI** (later shown weak).

**Sunset:** many nets shut **3G before 2G**. US majors ~2022.

---

## 6. 4G — All-IP LTE

**ITU-R IMT-Advanced (2008):** all-IP · **~100 Mbit/s** high mobility / **~1 Gbit/s** low mobility · 5–20 MHz (opt. 40) channels.

First **LTE** and Mobile WiMAX missed the 1 Gbit/s bar; ITU still allowed “4G” as forerunners. **LTE-Advanced** / **802.16m** = full IMT-Advanced. Qualcomm **dropped UMB**; industry stacked on LTE.

**Break from 3G:** **OFDMA** DL, **SC-FDMA** UL · **MIMO** · no circuit voice → **VoLTE** · IPv6.

**First public LTE:** TeliaSonera, Stockholm/Oslo, **14 Dec 2009**. **TD-LTE** for China and TDD markets. WiMAX lost to LTE.

Operators: LTE = “4G”, LTE-A / CA = “4G+”.

---

## 7. 5G — IMT-2020, New Radio

Market 5G = **3GPP 5G System + NR** (Rel-15+), aimed at **IMT-2020**.

**NSA:** NR + **4G EPC** (how most launched). **SA:** dedicated **5G Core** (slicing, URLLC, **VoNR**).

**ITU triangle:** **eMBB** (what phones use) · **URLLC** (factory / V2X-class) · **mMTC** (mass IoT).

**RAN/core:** massive MIMO, beamforming, small cells; polar + LDPC (not 4G turbo); SBA core, SDN/NFV, slicing, edge. Not every net has all of this on.

**3GPP ranges (generation still not “the GHz number”):** **FR1** 410 MHz–7.125 GHz (coverage + most capacity; mid-band **~3.5 GHz** is the workhorse) · **FR2** 24.25–71 GHz mmWave (short, multi-gigabit).

**Launch:** South Korea **3 Apr 2019**; Verizon same day (limited). Real downloads: **hundreds of Mbit/s**, not 20 Gbit/s peaks. Also FWA, private 5G. Caveat: eMBB-first; URLLC/mMTC often still a roadmap.

---

## 8. After 5G (one paragraph)

**6G / IMT-2030** is not a deployed generation. 3GPP is on 5G Advanced and early 6G study; commercial talk is **early 2030s**. Aims: rate, latency, energy, AI-native RAN, NTN. Not the subject of this case study.

---

## 9. Generation timeline

```
1979–83   1G  analog cellular (NTT, NMT, AMPS)
1991      2G  GSM (then cdmaOne 1995); SMS
~2000     2.5/2.75G  GPRS / EDGE
2001      3G  IMT-2000 (FOMA; EV-DO 2002); then HSPA
2009      4G  LTE (IMT-Advanced path); VoLTE later
2019      5G  NR + NSA, then SA 5GC
2030s     6G  planned (out of scope)
```

---

## 10. Conclusions

1. The story is **network generations**, not radio-in-general: analog FM → digital GSM/cdmaOne → WCDMA/HSPA → **OFDMA all-IP LTE** → **NR + 5GC**.  
2. **ITU** names the generation; **3GPP / 3GPP2** specify it.  
3. Each G buys a new **service** (voice → SMS → mobile web → HD/VoLTE → eMBB/slicing) at the cost of new infrastructure.  
4. **Sunsets are not 1-2-3-4-5:** 3G often dies before 2G.  
5. **G ≠ GHz.** Akashvani is broadcast, not a G.

---

## 11. References

- `wikipedia-1g.md` … `wikipedia-5g.md` ([1G](https://en.wikipedia.org/wiki/1G)–[5G](https://en.wikipedia.org/wiki/5G)); brief [6G](https://en.wikipedia.org/wiki/6G)  
- `chatgpt-2.4ghz-vs-2g-misconception.md`  
- [All India Radio](https://en.wikipedia.org/wiki/All_India_Radio)

Verify dates/rates against the live article or 3GPP/ITU if submitting formally.
