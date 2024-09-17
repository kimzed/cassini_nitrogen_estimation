
💎 Idea
Emisat: Innovative NOx Emission Reporting

Corporate Sustainability Reporting Directive (CSRD) from the European Union is set to impact nearly 50,000 companies across the EU, mandating comprehensive disclosure of environmental, social, and governance (ESG) impacts. This new standard requires reporting on how activities affect climate, human rights, and pollution.

At Emisat, we focus on providing cheap, fast, and scalable NOx emission reporting for specific locations. Our innovative approach adresses the issue of costly on-site measurements and imprecise satellite data, offering a solution that's both accurate and accessible.

Through Emisat's services, companies can transition from reactive to proactive environmental management, ensuring compliance with CSRD and contributing to a cleaner, more sustainable future.



🛰️ EU space technologies
Emisat harnesses the power of EU space technologies and geospatial data by using Sentinel-5P NRTI NO2 and Global Forecast System wind data. We combine these datasets using state-of-the-art physical modeling approaches based on scientifical research. We provide high-resolution NOx emission estimates with improved spatial granularity compared to current methods. We leverage the solution proposed by Beirle, S., Borger, C., et al. (2019). “Pinpointing nitrogen oxide emissions from space.”.

Our innovative use of satellite measurements and wind data allows us to pinpoint specific emission sources like power plants, rather than just measuring raw NO2 levels. We also propose to track impact of this pollution on nearby communities.



⛑️ Emisat directly addresses the following challenge:
Challenge #1: Emissions and carbon footprint reporting

Emisat provides an effective solution for carbon accounting and reporting by:

Offering precise NOx emission reporting, a crucial component of overall carbon footprint.
Using European space data from Copernicus (Sentinel-5P).
Enabling companies to track and manage their emissions effectively, fostering accountability and promoting sustainability.
Supporting compliance with CSRD and other environmental regulations.
Contributing to the collective effort to mitigate climate change through better emission monitoring and management.

💰Business plan 
estimate Funding Needed: €500,000

Use of Funds:

Software Development: €200,000
Operational Expenses: €150,000
Marketing and Sales: €100,000
Working Capital: €50,000
Revenue streams:

SaaS Platform:

Pricing: €500 per customer per month
Features:
Emission detection and measurement
Real-time reporting
Impact tracking on nearby communities
Consultancy Services:

Pricing: €10,000 per project
Services:
Developing mitigation strategies
Tailored compensation plans for affected communities
Regulatory compliance assistance
Year 1 Projections:

SaaS Revenue:
Total Customers: Starting at 5, growing to 17 by year-end
Total Revenue: €63,000
Consultancy Revenue:
Projects: 10
Total Revenue: €100,000
Total Revenue: €163,000
Expenses:
Operational Costs: €360,000
Net Profit/Loss: -€197,000
Year 2 Projections:

SaaS Revenue:
Total Customers: Growing from 17 to 55
Total Revenue: €204,000
Consultancy Revenue:
Projects: 12
Total Revenue: €120,000
Total Revenue: €324,000
Expenses:
Operational Costs: €420,000
Net Profit/Loss: -€96,000
Year 3 Projections:

SaaS Revenue:
Total Customers: Growing from 55 to 174
Total Revenue: €652,000
Consultancy Revenue:
Projects: 14
Total Revenue: €140,000
Total Revenue: €792,000
Expenses:
Operational Costs: €480,000
Net Profit/Loss: €312,000
Break-even Analysis:

Cumulative Losses (Years 1-2): -€293,000
Year 3 Profit: €312,000
Cumulative Profit: €19,000 (Break-even achieved in Year 3)
Customer Acquisition Plan:

Estimated CAC: €2,000
Growth Strategy: Begin with local markets, then expand regionally and internationally


🛠️ Get money the service
Emisat provides the following services:

Software as a Service (SaaS):
Post a start and end date and a coordinate polygon to our API
Our backend model processes the emission data
Receive a comprehensive emission report
Subscription-based pricing: Pay for what you need, when you need it
Consultancy services:
Partner with experts to help mitigate and compensate for your emissions
Our services are tailored for various client groups:

Heavy industry for reporting and compliance purposes
Consultancy companies working on CSRD reporting


🗺️ Roadmap
Improve current approach for better accuracy, potentially incorporating Machine Learning techniques
Expand to methane and CO2 estimation, possibly deriving from nitrogen emission reports
Pursue European certification and cooperation for CSRD compliance
Recruit an atmospheric scientist in the team
expansion to new markets:

Livestock farmers
Governmental agencies (e.g., for fraud detection)
🤼 Team
Cédric Baron: French geo-data scientist with a degree from Wageningen University. Currently working as an ML engineer at Avanade Netherlands.
Valeriy Litkovskyy: A passionate and skilled full-stack software developer willing to deliver the best possible products. Currently working at Intex System. Designing a reliable and scalable architecture for the next generation solution to the climate change dilemma.
Antonio Luca: A mechanical engineer with automation as the main driver of his activity and a background in data analysis on MEMS devices. An avid reader always seeking new challenges in international contexts, bringing strong technical skills and passionate about sustainable innovation.
Alice Giacomelli: Dynamic and curious with a strong passion for innovation and business support. Matured experience in banking consultancy and commercial banking. Always seeking new opportunities in private equity and venture capital. Easily adaptive to complex environments, striving for simple and effective solutions to achieve ambitious goals
Davide Bencivenga: Bringing a mix of technical understanding and strategic insight, with a background in industrial engineering and a passion for generative AI. Focused on delivering innovative, commercially viable solutions.
Alberto Ambrosini: A curious person, with a strong entrepreneurial sense. Background in economics, law,  management, and finance. Well versed with working in collaborative and interdisciplinary environments. Extremely extrovert, skilled in networking, able to manage stakeholder, investors relationships, organize events, scout for partnership and growth opportunities. Natural at sales and marketing.




Appendix: physical modelling
Our model combines knowledge from top-down emission maps with wind fields from ECMWF, to average horizontal fluxes of NO2 which preserve strong gradients at point sources.

The NOx flux is given by: F = L*V*w

Where L is NOx divided by NO2, V corresponds to NO2 tropospheric column and w corresponds to wind fields

The divergence of the flux yields to emissions (E) and sinks (S), from continuity equation at steady state: D = E - S

We can describe the sinks by a 1st order time constant: S = L*V/τ, where τ is the time constant for the degradation of NOx gas. 

Emissions are calculated as follows: E = D + S = ∇(L*V*w) + L*V/τ

As divergence is a linear operator, the mean emission is determined by the temporal mean sinks and the divergence of the temporal mean flux.

Thanks to the divergence method and by applying a peak fitting algorithm , we can provide a clear localisation of point sources (e.g., power plants, cement plants) with an accuracy below 2km.

Emissions uncertainty due to V, L and τ uncertainties in optimal conditions is 42% (detection limit: 0.03 kg/s), while it can go up to 65% in case of lower sensitivity and sample sizes (detection limit: 0.11 kg/s). Measurements with cloud data fraction above 30% were skipped.

