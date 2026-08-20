# 5G

Source: https://en.wikipedia.org/wiki/5G

Plain-text extract from English Wikipedia (via MediaWiki API).

---

5G is the fifth and current generation of cellular network technology and the successor to 4G. In common commercial use, the term refers primarily to mobile networks based on the 3rd Generation Partnership Project (3GPP) 5G system and its New Radio (NR) air interface, which were first specified in 3GPP Release 15. 5G was developed to meet the International Telecommunication Union's IMT-2020 framework for fifth-generation mobile systems. Large-scale commercial deployments began in 2019, including South Korea's national 5G rollout. 5G networks may be deployed in non-standalone mode, using existing LTE core-network infrastructure, or in standalone mode with a dedicated 5G Core.
Like earlier cellular systems, 5G networks divide service areas into smaller zones called cells, which are served by fixed cell sites. Compatible devices connect by radio to local base stations, which are linked to an operator's core network and to external networks such as the Internet through backhaul connections. 5G can be deployed using low-band, mid-band, and high-band radio spectrum, with coverage and performance depending heavily on the frequencies used, network design, congestion, and device capabilities.
Compared with 4G, 5G is designed to provide higher data rates, greater network capacity, lower latency, improved support for dense device deployments, and more flexible network management. For IMT-2020 radio-interface evaluation, the ITU specified peak data-rate requirements of 20 Gbit/s downlink and 10 Gbit/s uplink under ideal conditions, as well as latency and connection-density targets for enhanced mobile broadband, ultra-reliable low-latency communications, and massive machine-type communications. Actual user speeds are typically much lower than peak values and vary by operator, location, spectrum band, signal quality, and network load.

5G is used for mobile broadband, fixed wireless access, private and industrial networks, and machine-type communications. Its standards support features such as network slicing, edge computing, non-public networks, and ultra-reliable low-latency services, although these capabilities are not present in every deployment. The rollout of 5G has required new spectrum allocations and upgrades to radio access, transport, and core-network infrastructure. It has also raised issues involving deployment cost, energy use, vendor security, and public claims about radio-frequency health effects. 5G is being deployed alongside 4G networks and is expected to coexist with them for many years.


== History ==


=== Early research (2008–2012) ===
In 2008, NASA and the Machine-to-Machine Intelligence Corporation (M2Mi) conducted nanosatellite communication studies that influenced early next-generation network concepts.  
In 2012, New York University established NYU Wireless, a research center focused on millimeter-wave communication. The same year, the University of Surrey founded the 5G Innovation Centre, funded by £35 million from public and industry partners including Huawei and Samsung. Also in 2012, the European Union launched the Mobile and Wireless Communications Enablers for the Twenty-Twenty Information Society (METIS) project to align emerging network research with international standardization.  


=== Standardization and early trials (2013–2018) ===
In 2013, the ITU-R Working Party 5D began studies on IMT-2020, later formalized as the 5G standard.  
During the same period, major firms such as Samsung Electronics, NTT Docomo, and Huawei conducted early trials. Samsung tested a prototype achieving more than 1 Gbit/s across 2 km using 8 × 8 MIMO antennas. NTT Docomo received a government award at CEATEC for high-speed network development, while Huawei announced a US$600 million program to advance mobile network technology.  


=== Commercial rollout (2019–2021) ===
On April 3, 2019, South Korea launched its national network, the first full commercial deployment. Hours later, Verizon began limited service in select U.S. cities. In June 2019, Globe Telecom introduced the Philippines' first next-generation network, and in December 2019, AT&T launched a consumer service in the United States that expanded nationwide during 2020.  
Commercial 5G deployment expanded rapidly through 2020. Beyond public mobile networks, it was also adopted in private industrial and enterprise systems, including operation in unlicensed spectrum (NR-U) and licensed non-public networks (NPNs). Private 5G networks became important for Industry 4.0 automation and smart manufacturing. Early rollouts used non-standalone (NSA) mode—with 4G cores—before networks transitioned to standalone (SA) mode with dedicated 5G cores.
South Korea's 2019 rollout used equipment from Samsung, Ericsson, and Nokia; LG U Plus also deployed Huawei hardware.  
Samsung supplied most of the roughly 86,000 sites, while SK Telecom, KT Corporation, and LG U Plus concentrated coverage in major cities using the 3.5 GHz band under NSA operation. Reported download speeds averaged 200–400 Mbit/s, and subscriptions grew from about 260,000 to 4.7 million during 2019.  
Following these early deployments, T-Mobile US launched the first nationwide standalone network in 2020. Ericsson projected that by the mid-2020s, 5G networks would reach about 65 percent of the global population.
Major suppliers of 5G radio and core systems included Altiostar, Cisco Systems, Datang Telecom/Fiberhome, Ericsson, Huawei, Nokia, Qualcomm, Samsung, and ZTE. Huawei was estimated to hold about 70 percent of global 5G base stations by 2023.


=== Recent developments (2022–present) ===
By 2022, network speeds in many regions had stabilized, and operators began testing 5.5G upgrades to improve capacity and latency. By the early 2020s, large-scale commercial 5G networks were active across most developed markets, and rollout in developing regions was still accelerating.


== Technologies ==


=== Small cells ===

Small cells are low-power radio nodes that extend network capacity in dense or indoor areas. They operate over short distances, typically a few dozen to a few hundred metres, and are used to maintain coverage for mmWave signals.


=== Massive MIMO ===

Massive multiple-input multiple-output (MIMO) systems use large antenna arrays to increase capacity and spectral efficiency. They extend conventional MIMO by serving multiple users simultaneously and steering signals toward them to reduce interference.


=== Beamforming ===

Beamforming directs radio energy toward specific users. In analogue beamforming, antenna outputs are combined to focus signal power in one direction. Digital beamforming transmits data streams across multiple layers to improve signal strength and reliability.


=== Non-orthogonal multiple access (NOMA) ===
Non-orthogonal multiple access assigns different power levels to users sharing the same frequency resources to improve spectral efficiency.


=== Channel coding ===
5G NR uses polar codes for control channels and low-density parity-check codes (LDPC) for data channels, replacing the turbo codes used in 4G.


=== Research in to wireless power ===
Research has explored the use of 5G mmWave networks for wireless power transfer. Studies using wavelengths between 1 mm and 10 mm remain experimental.


== Core network architecture ==
The 5G core (5GC) is a service-oriented, software-defined system that separates control and user planes and supports flexible deployment. It replaces the 4G Evolved Packet Core with modular, software-based network functions.


=== Software-defined networking and virtualization ===

Software-defined networking (SDN) and network function virtualization (NFV) enable software-based configuration, scaling, and management of networks. Together with network slicing, these technologies support applications such as the Internet of things, connected vehicles, and industrial automation.


=== Service-based architecture (SBA) ===
Service-based architecture (SBA) integrates SDN and NFV principles and replaces the 4G EPC framework with modular network functions that communicate through RESTful APIs. Each function registers with a network repository function (NRF), which enables independent scaling and interoperability.


=== Core network functions ===
Each network function performs a defined role within the 5G core, replacing or extending elements from the 4G EPC.


=== Supporting components ===
Additional components manage roaming and inter-network connectivity:

Non-3GPP Interworking Function (N3IWF)
Security Edge Protection Proxy (SEPP)
Trusted Non-3GPP Gateway Function (TNGF)
Trusted WLAN Interworking Function (TWIF)
Wireline Access Gateway Function (W-AGF)


== Frequency bands and coverage ==

5G networks use multiple parts of the radio spectrum. They operate across three main frequency ranges—low, mid, and high bands—which balance speed, coverage, and signal quality differently.
Between 2016 and 2019, regulators in many regions, including the United States and the European Union, reallocated large sections of spectrum for 5G through auctions and new licensing rules. By 2019, more than 50 countries had assigned or planned to assign 5G frequencies. In 3GPP Release 16, the standard added 5G NR-U, allowing operation in both unlicensed and licensed spectrum.


=== Frequency ranges ===
The 5G New Radio (NR) interface defines two main operating ranges:

Frequency Range 1 (FR1) – 410 MHz to 7.125 GHz, also called sub-6 GHz. It covers low- and mid-band frequencies and supports channel bandwidths up to 100 MHz. Typical download speeds range from 5 to 900 Mbit/s depending on conditions.
Frequency Range 2 (FR2) – 24.25–71 GHz, known as millimeter wave or high band. It supports wider channel bandwidths—up to 400 MHz per carrier—and can reach multi-gigabit data rates. These signals travel only short distances and are easily blocked by walls, windows, and vegetation, so FR2 is mainly used in dense urban areas such as stadiums and city centers.


=== Coverage and signal behavior ===
Low- and mid-band 5G provide broad coverage and reliable indoor reception.  
High-band signals weaken rapidly and may lose over 100 dB when passing through common building materials. Operators use beamforming antennas, small cells, and signal repeaters to extend range and improve indoor coverage.


=== Wi-Fi integration ===
Technologies such as License Assisted Access (LAA) and LTE-WLAN Aggregation (LWA) let mobile networks share unlicensed spectrum with Wi-Fi. Cloud-based RAN systems and dense small-cell layouts help narrow the performance gap between cellular and Wi-Fi links.


== Application areas ==
The ITU-R defines three main application areas for 5G: enhanced mobile broadband (eMBB), ultra-reliable low-latency communications (URLLC), and massive machine-type communications (mMTC). These categories describe the main uses of 5G: faster mobile connections (eMBB), highly reliable and responsive communication (URLLC), and large-scale links between machines (mMTC). By 2020, eMBB was widely deployed, while URLLC and mMTC were still in development.


=== ITU-R categories ===
Enhanced mobile broadband (eMBB) provides much faster internet and higher capacity than 4G. It supports intensive data use in busy areas such as city centres, stadiums, and transport hubs.  
Ultra-reliable low-latency communications (URLLC) are designed for time-critical applications such as factory automation, remote medical procedures, and traffic systems. Shorter transmission delays improve precision and reliability.  
Massive machine-type communications (mMTC) connect large numbers of low-power devices such as sensors and meters. These networks underpin the Internet of things (IoT) by allowing machines to exchange data autonomously in industry, transport, and urban systems.


=== Industrial applications ===
5G is used in transport, manufacturing, and energy systems that require constant, low-latency communication. The 5G Automotive Association develops vehicle-to-everything (C-V2X) standards that allow cars to exchange safety information with nearby vehicles and infrastructure. Drones and autonomous vehicles use 5G for navigation, remote control, and real-time data transmission. Low-latency connections also enable digital twin models—virtual copies of machines or buildings that show real-time performance data used for monitoring and maintenance.


=== Public and commercial services ===
5G extends to public safety, broadband access, and media delivery. Emergency services use it for live video, data, and reliable push-to-talk communication. Fixed wireless access (FWA) provides home and business broadband using 5G radio links instead of wired connections, especially in rural areas where laying cables is costly.  5G Broadcast trials in Europe show that local 5G networks can deliver live television and radio to many devices simultaneously without using mobile data plans. Voice over NR (VoNR) allows phone calls to be made over 5G's internet-based network, similar to Voice over LTE (VoLTE) on 4G.


== Performance ==


=== Speed ===
5G can deliver much higher data rates than 4G, up to ten times faster. Theoretical peak download speeds reach up to 20 Gbit/s. In practice, average 5G download speeds in the United States have been measured at about 186 Mbit/s by T-Mobile, while South Korea in 2022 led globally with averages near 430 Mbit/s. 5G networks are also designed to provide much greater total capacity and efficiency than 4G, with up to a hundredfold projected increase.
The most widely deployed version, sub-6 GHz (mid-band) 5G, provides speeds of roughly 10–1000 Mbit/s with wider reach than mmWave bands. C-Band (n77/n78) was introduced in the U.S. in 2022, though activation by Verizon and AT&T was briefly delayed due to FAA safety concerns. The highest 5G speed measured in a deployed network is 5.9 Gbit/s (2023). Low-band frequencies such as n5 cover larger areas per cell but deliver lower data rates of around 5–250 Mbit/s.


=== Latency ===
Typical air latency for 5G is around 8–12 ms, excluding retransmissions and handovers. Verizon reported about 30 ms latency in early deployments. Edge servers located near base stations can reduce round-trip time to roughly 14 ms and minimize jitter to about 1.8 ms. Latency increases substantially during handovers, ranging from 50 to 150 ms depending on network conditions. Ongoing research focuses on reducing these interruptions by adjusting handover margins and time-to-trigger parameters.


=== Error rate ===
5G uses adaptive modulation and coding schemes (MCS) to maintain a low block error rate (BLER). When the error rate exceeds a threshold, the system automatically switches to a lower MCS to prioritize reliability over speed.


=== Range ===
The range of 5G varies with transmit power, frequency, and interference.
High-frequency mmWave bands (e.g., n258) have a shorter range than mid-band (n78), which in turn has a shorter range than low-band (n5). Operators use network simulation and drive testing to measure the actual range and coverage of these bands, as real-world performance can differ from marketing claims.


== Standards ==
The term 5G was first associated with the International Telecommunication Union's IMT-2020 standard. It defines peak download and upload rates of 20 and 10 Gbit/s.
The 3rd Generation Partnership Project (3GPP) later proposed its 5G New Radio (NR) technology for IMT-2020.


=== Frequency ranges ===
5G NR operates in two bands:

FR1 (Sub-6 GHz; 410 MHz to 7.125 GHz): low and mid-band frequencies with wide coverage and moderate speeds.
FR2 (24.25 GHz to 71 GHz): millimeter-wave (mmWave; higher) frequencies with higher speeds but shorter range.
Early FR1 deployments reusing 4G infrastructure (non-standalone mode) have been reported to provide 15–50 percent higher throughput than advanced 4G networks under favorable conditions.


=== Network deployment modes ===
5G networks can operate in Non-Standalone (NSA) mode using existing LTE infrastructure or Standalone (SA) mode using a dedicated 5G Core (5GC) network.


=== 3GPP specifications ===
3GPP and ETSI publish key technical specifications, including:

TS 23.501 – system architecture for the 5G system (5GS)
TS 24.501 – Non-Access-Stratum (NAS) protocol for 5GS
TS 23.003 – numbering, addressing and identification
TS 26.131 – terminal acoustic requirements for telephony; Requirements
TS 26.132 – Speech and video telephony terminal acoustic test specification
TS 26.441 – Codec for Enhanced Voice Services; General Overview


=== Other standardization bodies ===
Other organizations also contribute to 5G standards.
The DECT-2020 specification defines DECT NR+, a non-cellular, mesh-based radio system recognized by ITU as part of 5G.
The IEEE defines standards for wired links between the remote radio unit (RRU) and the baseband unit (BBU). 

IEEE 1914.1 describes the architecture of the fronthaul network connecting these components
IEEE 1914.3 defines an Ethernet format for transmitting I/Q data based on 3GPP functional splits


=== 5Gi ===
5Gi was developed in India by IIT Madras, IIT Hyderabad, the Telecommunications Standards Development Society India (TSDSI) and the Centre of Excellence in Wireless Technology (CEWiT). It extends 5G coverage in rural and remote areas through low-mobility large-cell (LMLC) configurations. 5Gi was merged in April 2022 into the global 5G NR standard in 3GPP Release 17.


=== Internet of things ===
In the Internet of things (IoT), 3GPP defines the evolution of NB-IoT and eMTC to support low-power wide-area applications such as connected sensors and meters.


=== Voice over NR (VoNR) ===

3GPP standards also define advanced communication services for voice and connected devices.
3GPP defines Voice over NR as a technology that enables native, high-quality voice over a 5G Standalone network through the 5G System Architecture. Unlike early 5G Non-Standalone deployments that relied on Evolved Packet System Fallback, VoNR integrates directly with the IP Multimedia Subsystem (IMS) used in VoLTE. It uses NAS protocols to establish high-priority QoS flows that support URLLC requirements for voice traffic. Support for 5G Standalone is a prerequisite for VoNR. VoNR benefits from the enhanced security architecture of the 5G Core network, including improved subscriber identity protection. VoNR delivers superior audio quality through the Enhanced Voice Services (EVS) codec, which must adhere to rigorous terminal acoustic requirements and standardized testing procedures.
Most phones released since 2023 (such as the iPhone 15 series and newer flagship devices) support VoNR, but availability depends on carrier enablement in specific areas.


=== Non-terrestrial networks ===
3GPP also defines non-terrestrial networks (NTN) that use satellites and airborne platforms to provide coverage where ground networks are impractical. In 2024, the European Space Agency demonstrated the first ground 5G NTN connection to a low earth orbit (LEO) satellite from horizon to peak to horizon elevations using the Ka-band frequency range.


=== 5G-Advanced ===
5G-Advanced, also known as 5.5G or 5G-A, is defined in 3GPP Release 18 as a transition between 5G and 6G. It adds features for more efficient spectrum use, lower energy demand, and higher reliability. The release introduces AI- and ML-based network management, extended-reality services, and communication support for autonomous systems.
Release 18 specifies improved time-synchronization methods independent of the GNSS and built-in geolocation functions. It extends non-terrestrial support to satellite and airborne communication.


=== 5G RedCap ===
5G Reduced Capability (RedCap) in 3GPP Release 17 is designed to bridge the gap between high-performance 5G devices and low-power IoT technologies such as LTE-M and NB-IoT. It was created to address use cases between Enhanced Mobile Broadband (eMBB), Ultra-Reliable Low-Latency Communications (URLLC), and Massive Machine-Type Communication (mMTC) technologies.


== 5G hardware ==

The Global Mobile Suppliers Association (GSA) compiled the first database of 5G-compatible products, listing 23 manufacturers and 33 models across categories such as smartphones, hotspots, and customer-premises equipment. Later surveys recorded more than one hundred announced products from over fifty vendors.
Early 5G modem chipsets were released by Intel, MediaTek, Qualcomm, and Samsung, followed by additional platforms in subsequent product generations.
The Samsung Galaxy S10 5G was among the first smartphones to support 5G networks. Other early 5G models included the Nokia 8.3 5G, designed for operation across low- to mid-band frequencies; the Google Pixel 5 and Pixel 4a (5G); and Apple's iPhone 12 series, the company's first generation with 5G capability.

By the early 2020s, most high-end smartphones featured 5G capability, while some consumer devices still lack full support. As a result, the practical benefits for mid range phone users have been modest, and 5G adoption has lagged behind expectations.


== Security risks ==


=== Network and protocol risk ===
In 2019, the European Commission and the European Union Agency for Cybersecurity (ENISA) warned that 5G networks could expand potential attack surfaces for state actors, recommending diversification of suppliers. Nokia and Ericsson are the only European manufacturers.
Researchers from ETH Zurich and partner universities found weaknesses in the 5G authentication process that could expose users to new security risks. They concluded that the system was still immature and that its higher data capacity could increase exposure to attacks.
A 2022 study identified a design flaw in the Evolved Packet System (EPS) that could affect device behavior during network switching.


=== Internet of things risk ===
Growth of the Internet of things increases the number of devices connected through 5G. IoT Analytics estimated growth from about 7 billion devices in 2018 to over 21 billion by 2025, raising exposure to DDoS attacks, cryptojacking, and other cyberattacks.


=== Espionage and supply chain risk ===
Concerns about espionage and data access have influenced national policies. The United States, Australia, and the United Kingdom have restricted or banned Chinese-made equipment.
A 2012 report by the United States House Permanent Select Committee on Intelligence concluded that equipment from Huawei and ZTE could pose national-security risks. Later assessments by U.S. intelligence agencies warned that Huawei products could allow covert data access. In 2022, the FBI reported that Huawei equipment near U.S. military bases could interfere with nuclear communications.
Huawei and the Chinese government deny the allegations. Analysts note that China's National Security Law could require companies to provide data to authorities if requested.
In 2020, the United States Department of State launched The Clean Network initiative to promote data privacy and security among allied nations. By year-end, more than 60 countries and 200 telecommunications companies had joined, including most NATO, EU, and OECD members.


== Interference issues ==


=== Weather and satellite data ===
Some 5G bands, such as n258 at 26 GHz, are close to frequencies used for passive remote sensing by weather and Earth observation satellites, including water vapor measurements at 23.8 GHz. Interference with satellite observations could reduce the accuracy of numerical weather prediction models and affect sectors such as commercial aviation.
NASA, NOAA, and the U.S. Navy warned that out-of-band emissions from 5G transmissions near 24 GHz could degrade forecasts by up to 30 %. The 2019 World Radiocommunication Conference set an interim limit of −33 dBW until 2027, followed by −39 dBW. The World Meteorological Organization (WMO) and European Centre for Medium-Range Weather Forecasts (ECMWF) warned that these limits could reduce forecast reliability.


=== Aviation systems ===
In 2021–2022, the Federal Aviation Administration (FAA) warned that some 5G signals could interfere with aircraft radar altimeters, which operate at 4.2–4.4 GHz, while new 5G services use 3.7–4.0 GHz. Europe uses lower frequencies (3.4–3.8 GHz), reducing the risk.


=== Satellite communication ===

Some 5G allocations overlap with frequencies used by C band satellite communication systems. Interference can occur when networks operate in 3.3–3.6 GHz, near satellite reception at 3.4–4.2 GHz Mitigation uses low-noise block downconverters and waveguide filters.


=== Wi-Fi coexistence ===
5G and Wi-Fi 6E share the 6 GHz band, which enables efficient spectrum use but requires coordination to prevent interference. Both operate under unlicensed conditions in the US and EU, supporting NR-U and Wi-Fi 6E technologies.


== Public perception ==
Analysts note that marketing of 5G has often overstated its capabilities. Common concerns include limited user benefits, short range of mmWave signals, and rebranding of non-5G improvements as 5G.
A 2020 survey by McKinsey & Company found that operators identified few immediately profitable use cases. Consumer surveys show mixed attitudes, with skepticism about marketing claims and uneven coverage in early deployments. Industry groups and network operators state that 5G enables faster speeds and lower latency, though results depend on infrastructure rollout and available spectrum. In contrast to the initial excitement about the prospects, many firms striving for deployment have encountered reality, users are not eager to upgrade the technology. Five years after its launch, a majority of users have yet to transition to the new standard.


== Misinformation ==


=== Health claims ===

Public concern about the effects of wireless signals predates 5G technology. Similar concerns were raised about earlier mobile standards in the 1990s and 2000s. According to the Centers for Disease Control and Prevention (CDC), "exposure to intense, direct amounts of non-ionizing radiation may result in tissue damage due to heat. This is uncommon and mainly a workplace concern for those working with large sources of non-ionizing radiation."
Some critics argue that existing exposure limits are too lenient or influenced by industry lobbying. Claims that the use of 5G mobile networks can cause cancer are unsupported by scientific evidence.
Several books making unverified claims about wireless health effects have been published. One, by Joseph Mercola, alleged links to ADHD, heart disease, and brain cancer. Mercola was criticized for promoting misinformation during the COVID-19 pandemic and warned by the Food and Drug Administration (FDA) for selling unapproved COVID-19 cures.
According to The New York Times, controversy regarding 5G health effects partly originated from an unpublished 2000 report by physicist Bill P. Curry for the Broward County School Board, which incorrectly concluded that higher-frequency microwaves are absorbed more deeply by the brain. Later analyses showed that this was a misunderstanding of in vitro research results. Experts noted that millimeter-wave frequencies used by 5G cannot penetrate the skin or reach internal organs. 
In a 2019 article, the same newspaper reported that RT America promoted claims linking 5G to diseases such as brain cancer, infertility, and Alzheimer's disease. The network aired several such programs in 2019, later cited by numerous blogs and websites.
In 2019, cities such as Brussels and Geneva temporarily halted 5G rollouts pending radiation assessments. The Swiss Telecommunications Association stated that studies had not demonstrated adverse health effects from 5G exposure.
Similar debates occurred in the Netherlands, the United States, and the United Kingdom, where some municipalities briefly delayed deployments or issued precautionary statements.
The Food and Drug Administration maintains that existing exposure limits for cellphone radiofrequency energy are sufficient to protect public health.
Low-level electromagnetic fields (EMF) can have measurable biological effects in plants and animals, but research remains inconclusive about health risks to humans. A 2019 meta-analysis found that while many in vitro and in vivo studies detected biological responses to radiofrequency exposure, the evidence did not establish health risks. 


==== COVID-19 conspiracy theories ====

The rollout of 5G technology began during the COVID-19 pandemic, prompting conspiracy theories that linked 5G to the pandemic.
These claims led to arson attacks on telecom masts in parts of Europe, including the Netherlands, the United Kingdom, and Italy. In the United Kingdom, at least 61 mobile masts were reportedly set on fire.
During the early months of the pandemic, Australian anti-lockdown protesters carried anti-5G signs, later connected to broader conspiracy groups. Two main versions of the conspiracy theory exist:

The first claims that radiation from 5G weakens the immune system, making people more vulnerable to SARS-CoV-2, the virus that causes COVID-19.
The second claims that 5G causes COVID-19. Some versions claim the pandemic hid illnesses blamed on 5G, while others suggest COVID-19 began in Wuhan, one of the first cities with early 5G rollout.


== Marketing of pre-5G technologies ==

The marketing of pre-5G technologies refers to the promotion of enhanced 4G networks as precursors or alternatives to 5G. Before and during early 5G deployment, some mobile network operators used terms such as "pre-5G", "5G-ready", "4.5G", and "5G Evolution" for upgraded LTE Advanced or LTE Advanced Pro networks. These networks could use features such as carrier aggregation, 256-QAM, and 4×4 MIMO to increase data rates, but they did not use 5G NR, the radio access technology standardized for 5G networks.
A notable example was 5G Evolution (5GE), introduced by AT&T in 2017 to market higher-speed LTE service with theoretical speeds up to 400 Mbit/s (40 Mbit/s real world), using 3-channel carrier aggregation, 4x4 MIMO and 256-QAM. AT&T described the service as "a foundation for our evolution to 5G while the 5G standards are being finalized", but technology publications criticized the branding as misleading because the underlying network remained based on LTE technologies rather than 5G.
In 2019, Sprint sued AT&T, alleging that the 5G Evolution and "5GE" branding misled consumers into believing that they were receiving 5G service. The dispute was later settled. In 2020, the National Advertising Review Board recommended that AT&T stop using "5G Evolution" and related claims in advertising, finding that the terms were misleading; AT&T said it disagreed with the decision but would comply with the self-regulatory process.


== References ==


== Further reading ==
Karipidis, Ken; Mate, Rohan; Urban, David; Tinker, Rick; Wood, Andrew (July 2023). "5G mobile networks and health—a state-of-the-science review of the research into low-level RF fields above 6 GHz". Journal of Exposure Science & Environmental Epidemiology. 31 (4): 585–605. doi:10.1038/s41370-021-00297-6. PMC 8263336. PMID 33727687.


== External links ==
 Media related to 5G at Wikimedia Commons
5G multi-antenna concepts
