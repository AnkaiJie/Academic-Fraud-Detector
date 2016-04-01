


import csv


'''
Created on Jan 05, 2016

@author: Ankai

NOTE: This CSV Writer was written for one specific author. It is hard-coded data for convenience
'''

import csv

'''
totalJournalDict = {' Wireless Networks': 67, ' Wireless networks': 18, ' Sensors': 13, ' … ': 11, ' Selected Areas in  …': 8, ' Wireless  …': 8, ' Multimedia Tools and Applications': 7, ' EURASIP Journal on  …': 6, ' EURASIP Journal on Wireless  …': 6, ' …  Surveys & Tutorials': 5, 'Wattar ': 4, ' EURASIP Journal on Wireless …': 4, ' Internet of Things  …': 3, ' Wireless Personal Communications': 3, ' Nano Communication Networks': 3, ' Signal Processing': 3, ' Vehicular Technology': 3, ' EURASIP Journal on Wireless Communications and  …': 3, ' Mobile Computing': 3, ' NanoBioscience': 2, ' Access': 2, ' Vehicular  …': 2, ' Systems Journal': 2, ' Communications  …': 2, ' 2015 ': 2, ' Sensors Journal': 2, ' Proceedings of the 8th  …': 2, ' Journal of Sensor and Actuator Networks': 2, ' Parallel and Distributed  …': 2, ' Mobile Networks and  …': 2, ' 计算机科学': 2, ' arXiv preprint arXiv: …': 2, ' …  in Biomedicine': 2, ' …  (GLOBECOM)': 2, 'Mougy': 2, ' Intelligent Transportation Systems': 2, ' Communications (ICC)': 2, ' INFOCOM': 2, ' Internet and Distributed  …': 2, ' International Journal of Distributed  …': 2, ' Proceedings of ACM The First Annual International  …': 2, ' Nanotechnology': 2, ' Eurasip journal on wireless communications …': 2, ' Journal of AI and Data  …': 2, ' Journal of Network and  …': 2, ' The Journal of Supercomputing': 1, ' The Scientific World  …': 1, ' Online Conference on …': 1, ' Proceedings of the  …': 1, ' Proceedings of the 2nd  …': 1, ' …  and Networks (ICCCN)': 1, 'Ibáñez': 1, ' …  and Networking Conference (WCNC)': 1, ' Wireless Networks ': 1, ' Global Information  …': 1, ' …  (MeMeA)': 1, ' …  Conference Fall (VTC  …': 1, ' Advances in Computing …': 1, ' Selected Areas in Communications': 1, ' …  (Cloudnet)': 1, ' International Journal of  …': 1, ' Network of the Future (NOF …': 1, ' Web Information Systems and Mining (WISM)': 1, ' Personal Indoor and Mobile  …': 1, ' Journal of Sensors': 1, ' Proceedings of the seventh ACM international  …': 1, ' High Performance Computing  …': 1, ' Green Technologies Conference …': 1, ' arXiv preprint arXiv:1102.2608': 1, ' Bio': 1, ' Future Generation Computer  …': 1, ' IEEE Transactions on  …': 1, ' arXiv preprint arXiv:1406.1867': 1, ' arXiv preprint arXiv:1408.2078': 1, ' Cloud Computing (CLOUD)': 1, ' Journal of Ambient Intelligence and Humanized  …': 1, ' IEEE Communications  …': 1, ' AAAI': 1, ' …  Sensor Systems': 1, ' Cloud Computing Technology …': 1, ' Parallel and Distributed Systems': 1, ' Computer Communications': 1, ' Mobile Networks and Applications': 1, ' Economics of Grids': 1, ' 电子学报': 1, ' ieeexplore.ieee.org': 1, ' INTERNATIONAL JOURNAL ON SMART  …': 1, ' Control': 1, ' Information Systems  …': 1, ' Multisensor Fusion and  …': 1, ' …  Systems (ICDCS)': 1, ' Journal of Computers': 1, ' Cloud Computing': 1, ' Pervasive Computing (ICPC)': 1, ' 软件学报': 1, ' 2011 ': 1, ' Network Protocols (ICNP)': 1, ' J Converg': 1, ' Computer Software and  …': 1, ' …  (BlackSeaCom)': 1, ' …  on Mobile Ad Hoc Networking and  …': 1, ' …  (VTC Spring)': 1, ' Network': 1, ' power': 1, ' Simulation Modelling Practice and Theory': 1, 'Saavedra': 1, ' Intelligent Transportation …': 1, ' Intelligent  …': 1, ' …  Workshops (ICC)': 1, ' Computer Science and  …': 1, ' Advance Computing Conference (IACC)': 1, ' KSII Transactions on Internet &  …': 1, ' International Journal of Control': 1, ' Artificial Intelligence Review': 1, ' Telecommunication Systems': 1, ' Proceedings of the 19th …': 1, ' Computational Problem': 1, ' TELKOMNIKA Indonesian Journal of …': 1, ' Computers & Electrical  …': 1, ' EURASIP Journal on Wireless Communications …': 1, ' Nano Communication  …': 1, ' Journal of Internet  …': 1, ' Green Communications and  …': 1, ' Intelligent Sensors': 1, ' 2013 IEEE 24th Annual International  …': 1, ' Journal of Network and Systems  …': 1, ' Pervasive Computing and  …': 1, ' e': 1, ' Computer Networks': 1, ' …  Conference (WCNC)': 1, ' Modeling & Optimization …': 1, ' 2010': 1, ' 计算机应用研究': 1, ' Innovative Mobile and Internet Services in  …': 1, ' Communications': 1, ' …  Assurance and Security (IAS)': 1, ' …  Processing and their …': 1, ' Journal of the American  …': 1, ' Wireless Days (WD)': 1, 'Valenzuela': 1, ' Journal of medical systems': 1, ' Information Theory and Applications  …': 1, ' Green Communications  …': 1, 'Rivera': 1, ' Communications Letters': 1, ' Sensor': 1, ' Signals': 1, ' Ad Hoc Networks': 1, ' Transactions on  …': 1, ' The Journal of  …': 1, ' ACM Transactions on  …': 1, ' Journal of Network and Computer Applications': 1, 'Wei': 1, ' Internet of Things Journal': 1, ' KTH Royal Institute of Technology': 1, ' International Journal of Antennas and Propagation': 1, ' Online Conference on Green Communications ( …': 1, ' Real': 1, ' EURASIP Journal on Wireless Communications  …': 1, ' Web Services (ICWS …': 1, ' International Journal On  …': 1, ' Communication Technologies for Vehicles': 1, ' Routing in Opportunistic Networks': 1, ' Wireless and Mobile  …': 1, ' …  Areas in Communications': 1, ' Cybernetics': 1, ' …  Networks and Self': 1, ' Computer  …': 1, ' BioNanoScience': 1, ' PhD dissertations': 1, ' …  Conference (VTC Spring)': 1, ' Multimedia tools and  …': 1, ' …  (CLOUD)': 1, ' Proceedings of the World Congress on  …': 1}


writer = csv.writer(open('dict.csv', 'w'))
for key, value in totalJournalDict.items():
    try:
        writer.writerow([key, value])
    except UnicodeEncodeError:
        continue 
'''

'''
indJournalArrays = [['Body area networks: A survey', {' …  Processing and their …': 1, ' Information Theory and Applications  …': 1, ' Journal of Network and  …': 1, ' Selected Areas in Communications': 1, ' Parallel and Distributed Systems': 1, ' Network': 1, ' …  in Biomedicine': 2, ' Multimedia Tools and Applications': 1, ' Journal of medical systems': 1, ' …  Assurance and Security (IAS)': 1, ' …  Surveys & Tutorials': 2, ' Journal of the American  …': 1, ' Computer Science and  …': 1, ' Cloud Computing Technology …': 1, ' Future Generation Computer  …': 1, ' Signal Processing': 1, ' Wireless  …': 1, ' Sensors': 4, ' Mobile Networks and  …': 1, ' EURASIP Journal on Wireless Communications …': 1, ' International Journal of Distributed  …': 1, 'Valenzuela': 1, ' The Journal of  …': 1, ' Systems Journal': 1, ' Multimedia tools and  …': 1}],

['A game-theoretic method of fair resource allocation for cloud computing services', {' INFOCOM': 1, ' Cloud Computing': 1, ' Parallel and Distributed  …': 1, ' Journal of Internet  …': 1, ' Web Information Systems and Mining (WISM)': 1, ' Computer Software and  …': 1, ' e': 1, ' Real': 1, ' The Scientific World  …': 1, ' Information Systems  …': 1, ' arXiv preprint arXiv:1102.2608': 1, ' 计算机科学': 2, 'Wei': 1, ' AAAI': 1, ' …  and Networks (ICCCN)': 1, ' Journal of Computers': 1, ' Green Technologies Conference …': 1, ' 电子学报': 1, ' …  (CLOUD)': 1, ' Economics of Grids': 1, ' TELKOMNIKA Indonesian Journal of …': 1, ' The Journal of Supercomputing': 1, ' Cloud Computing (CLOUD)': 1, ' Proceedings of the 2nd  …': 1, ' Multisensor Fusion and  …': 1, ' Journal of Network and Systems  …': 1, ' High Performance Computing  …': 1, ' Innovative Mobile and Internet Services in  …': 1, ' Internet of Things  …': 1}],

['Compressed data aggregation for energy efficient wireless sensor networks', {' INFOCOM': 1, ' Journal of Sensor and Actuator Networks': 1, ' …  Sensor Systems': 1, ' J Converg': 1, ' …  on Mobile Ad Hoc Networking and  …': 1, ' Signals': 1, ' Artificial Intelligence Review': 1, ' Network Protocols (ICNP)': 1, ' EURASIP Journal on Wireless Communications and  …': 1, ' Communications (ICC)': 1, ' EURASIP Journal on  …': 1, ' …  (MeMeA)': 1, ' Wireless Networks': 3, ' Communications Letters': 1, ' Ad Hoc Networks': 1, ' Wireless networks': 3, ' … ': 2, ' Sensors': 2, ' Computers & Electrical  …': 1, ' Sensor': 1, ' Advances in Computing …': 1, ' …  Systems (ICDCS)': 1, ' Eurasip journal on wireless communications …': 1, ' Internet of Things  …': 1}],

['A survey of green mobile networks: Opportunities and challenges', {' Green Communications and  …': 1, ' Wireless Networks': 3, ' Journal of Sensor and Actuator Networks': 1, ' Mobile Computing': 1, ' Proceedings of the 8th  …': 1, ' arXiv preprint arXiv:1406.1867': 1, ' Online Conference on …': 1, ' …  Networks and Self': 1, ' Communications  …': 1, ' power': 1, ' Computer Networks': 1, ' …  Surveys & Tutorials': 3, ' Vehicular Technology': 1, ' EURASIP Journal on Wireless  …': 1, ' Green Communications  …': 1, ' Online Conference on Green Communications ( …': 1, ' Modeling & Optimization …': 1, ' …  and Networking Conference (WCNC)': 1, ' Sensors': 2, ' Personal Indoor and Mobile  …': 1, ' 2013 IEEE 24th Annual International  …': 1, ' Wireless networks': 2, ' …  (Cloudnet)': 1, ' Systems Journal': 1}],

['Directional routing and scheduling for green vehicular delay tolerant networks', {' Wireless Networks': 11, ' EURASIP Journal on Wireless Communications  …': 1, 'Wattar ': 1, ' Internet and Distributed  …': 1, ' EURASIP Journal on Wireless  …': 2, ' Wireless networks': 7, ' Multimedia Tools and Applications': 2, ' Communications': 1, ' EURASIP Journal on  …': 2, ' EURASIP Journal on Wireless …': 1, ' 计算机应用研究': 1}],

['Routing for disruption tolerant networks: taxonomy and design', {'Ibáñez': 1, ' Journal of Network and  …': 1, ' Proceedings of the seventh ACM international  …': 1, ' EURASIP Journal on Wireless  …': 2, ' Routing in Opportunistic Networks': 1, ' KSII Transactions on Internet &  …': 1, ' 2010': 1, ' Mobile Computing': 1, ' Wireless Days (WD)': 1, ' Advance Computing Conference (IACC)': 1, ' Transactions on  …': 1, ' Wireless Networks': 5, ' Eurasip journal on wireless communications …': 1, ' Wireless Personal Communications': 1, ' Wireless networks': 2, ' Computer Communications': 1, ' Computational Problem': 1, ' Wireless  …': 1, ' Pervasive Computing and  …': 1, ' International Journal of Distributed  …': 1, ' Global Information  …': 1, ' 2011 ': 1, ' PhD dissertations': 1, ' Telecommunication Systems': 1}],

['Molecular communication and networking: Opportunities and challenges', {' Selected Areas in  …': 4, ' Nano Communication  …': 1, ' BioNanoScience': 1, ' NanoBioscience': 2, ' Proceedings of the 8th  …': 1, ' …  (BlackSeaCom)': 1, ' Signal Processing': 1, ' … ': 3, ' arXiv preprint arXiv: …': 2, ' Bio': 1, ' …  Workshops (ICC)': 1, ' Proceedings of ACM The First Annual International  …': 2, ' Nano Communication Networks': 3, ' Simulation Modelling Practice and Theory': 1, ' …  (GLOBECOM)': 2, ' Nanotechnology': 2, ' Sensors Journal': 1, ' Communications (ICC)': 1}],

['Routing metrics of cognitive radio networks: A survey', {' Wireless Networks': 14, ' Proceedings of the 19th …': 1, ' Wireless networks': 2, 'Mougy': 1, ' …  Conference (WCNC)': 1, ' Wireless  …': 2, ' Pervasive Computing (ICPC)': 1, 'Wattar ': 1, ' 2015 ': 1, ' Mobile Computing': 1, ' Proceedings of the World Congress on  …': 1, ' Internet and Distributed  …': 1, ' arXiv preprint arXiv:1408.2078': 1, ' EURASIP Journal on  …': 1, ' …  Conference (VTC Spring)': 1}],

['An adaptive geometry-based stochastic model for non-isotropic MIMO mobile-to-mobile channels', {' Intelligent Transportation …': 1, ' Selected Areas in  …': 4, ' Wireless Personal Communications': 1, ' Vehicular Technology': 2, ' Vehicular  …': 2, ' … ': 6, ' …  Areas in Communications': 1, ' IEEE Communications  …': 1, ' …  (VTC Spring)': 1, ' Signal Processing': 1, ' Wireless  …': 2, ' Mobile Networks and  …': 1, ' IEEE Transactions on  …': 1, ' Communication Technologies for Vehicles': 1, ' …  Conference Fall (VTC  …': 1, ' Intelligent Transportation Systems': 2, ' Intelligent  …': 1, ' International Journal of Antennas and Propagation': 1}],

['EDAL: An energy-efficient, delay-aware, and lifetime-balancing data collection protocol for heterogeneous wireless sensor networks', {' Wireless Networks': 12, ' Mobile Networks and Applications': 1, ' ieeexplore.ieee.org': 1, ' EURASIP Journal on Wireless  …': 1, ' Wireless networks': 1, ' International Journal of  …': 1, ' Wireless  …': 2, ' Journal of AI and Data  …': 1, ' Wireless Networks ': 1, ' EURASIP Journal on Wireless Communications and  …': 2, ' Multimedia Tools and Applications': 2, 'Rivera': 1, ' Access': 1, ' Sensors': 2, ' EURASIP Journal on Wireless …': 1}],

['A survey on topology control in wireless sensor networks: Taxonomy, comparative study, and open issues', {' Wireless Networks': 9, ' INTERNATIONAL JOURNAL ON SMART  …': 1, ' Parallel and Distributed  …': 1, ' Journal of Sensors': 1, ' Wireless Personal Communications': 1, 'Wattar ': 1, 'Mougy': 1, ' International Journal of Control': 1, ' Control': 1, ' Sensors Journal': 1, ' 2015 ': 1, 'Saavedra': 1, ' Computer  …': 1, ' KTH Royal Institute of Technology': 1, ' Cybernetics': 1, ' Multimedia Tools and Applications': 1, ' Journal of AI and Data  …': 1, ' Sensors': 2, ' EURASIP Journal on  …': 2, ' EURASIP Journal on Wireless …': 1}],

['A survey on the ietf protocol suite for the internet of things: Standards, challenges, and opportunities', {' Wireless Networks': 10, 'Wattar ': 1, ' Proceedings of the  …': 1, ' ACM Transactions on  …': 1, ' Wireless networks': 1, ' International Journal On  …': 1, ' Journal of Ambient Intelligence and Humanized  …': 1, ' Intelligent Sensors': 1, ' Sensors': 1, ' Web Services (ICWS …': 1, ' … (ICET)': 1, ' Wireless and Mobile  …': 1, ' Internet of Things Journal': 1, ' Communications  …': 1, ' Access': 1, ' Journal of Network and Computer Applications': 1, ' Multimedia Tools and Applications': 1, ' 软件学报': 1, ' Network of the Future (NOF …': 1, ' EURASIP Journal on Wireless …': 1, ' Internet of Things  …': 1}]
]

writer = csv.writer(open('inidividualJournals.csv', 'w'))
for paper in indJournalArrays:
    writer.writerow([paper[0]])
    for key, value in paper[1].items():
        try:
            writer.writerow([key, value])
        except UnicodeEncodeError:
            continue 
'''


'''
self_cite_arr = [{'Paper Title': 'Body area networks: A survey', 'Self Cites': 1},
{'Paper Title': 'A game-theoretic method of fair resource allocation for cloud computing services', 'Self Cites': 1},
{'Paper Title': 'Compressed data aggregation for energy efficient wireless sensor networks', 'Self Cites': 0},
{'Paper Title': 'A survey of green mobile networks: Opportunities and challenges', 'Self Cites': 1},
{'Paper Title': 'Directional routing and scheduling for green vehicular delay tolerant networks', 'Self Cites': 'No Valid PDF URL in GSC'},
{'Paper Title': 'Routing for disruption tolerant networks: taxonomy and design', 'Self Cites': 'No Valid PDF URL in GSC'},
{'Paper Title': 'Molecular communication and networking: Opportunities and challenges', 'Self Cites': 1},
{'Paper Title': 'Routing metrics of cognitive radio networks: A survey', 'Self Cites': 1},
{'Paper Title': 'An adaptive geometry-based stochastic model for non-isotropic MIMO mobile-to-mobile channels', 'Self Cites': 0},
{'Paper Title': 'EDAL: An energy-efficient, delay-aware, and lifetime-balancing data collection protocol for heterogeneous wireless sensor networks', 'Self Cites': 1},
{'Paper Title': 'A survey on topology control in wireless sensor networks: Taxonomy, comparative study, and open issues', 'Self Cites': 1},
{'Paper Title': 'A survey on the ietf protocol suite for the internet of things: Standards, challenges, and opportunities', 'Self Cites': 'No Valid PDF URL in GSC'}]

keys = self_cite_arr[0].keys()
with open('self_cites.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(self_cite_arr)
'''


'''
over_cite_arr = [[{'Citing Paper Number': 1, 'Over-cite Count': 1}, {'Citing Paper Number': 2, 'Over-cite Count': 1}, {'Citing Paper Number': 3, 'Over-cite Count': 1}, {'Citing Paper Number': 4, 'Over-cite Count': 4}, {'Citing Paper Number': 5, 'Over-cite Count': 1}, {'Citing Paper Number': 6, 'Over-cite Count': 1}, {'Citing Paper Number': 7, 'Over-cite Count': 0}, {'Citing Paper Number': 8, 'Over-cite Count': 4}, {'Citing Paper Number': 9, 'Over-cite Count': 1}, 'Paper Title: Body area networks: A survey'],

[{'Citing Paper Number': 1, 'Over-cite Count': 1}, {'Citing Paper Number': 2, 'Over-cite Count': 7}, {'Citing Paper Number': 3, 'Over-cite Count': 1}, {'Citing Paper Number': 4, 'Over-cite Count': 1}, {'Citing Paper Number': 5, 'Over-cite Count': 1}, {'Citing Paper Number': 6, 'Over-cite Count': 1}, {'Citing Paper Number': 8, 'Over-cite Count': 1}, {'Citing Paper Number': 9, 'Over-cite Count': 1}, 'Paper Title: A game-theoretic method of fair resource allocation for cloud computing services'],

[{'Citing Paper Number': 1, 'Over-cite Count': 1}, {'Citing Paper Number': 2, 'Over-cite Count': 4}, {'Citing Paper Number': 3, 'Over-cite Count': 1}, {'Citing Paper Number': 4, 'Over-cite Count': 2}, {'Citing Paper Number': 5, 'Over-cite Count': 2}, {'Citing Paper Number': 6, 'Over-cite Count': 1}, {'Citing Paper Number': 7, 'Over-cite Count': 0}, {'Citing Paper Number': 8, 'Over-cite Count': 1}, 'Paper Title: Compressed data aggregation for energy efficient wireless sensor networks'],

[{'Citing Paper Number': 2, 'Over-cite Count': 0}, {'Citing Paper Number': 3, 'Over-cite Count': 1}, {'Citing Paper Number': 4, 'Over-cite Count': 2}, {'Citing Paper Number': 5, 'Over-cite Count': 1}, {'Citing Paper Number': 6, 'Over-cite Count': 1}, 'Paper Title: A survey of green mobile networks: Opportunities and challenges'],

[{'Citing Paper Number': 1, 'Over-cite Count': 4}, {'Citing Paper Number': 2, 'Over-cite Count': 5}, {'Citing Paper Number': 3, 'Over-cite Count': 0}, {'Citing Paper Number': 4, 'Over-cite Count': 4}, {'Citing Paper Number': 5, 'Over-cite Count': 7}, {'Citing Paper Number': 6, 'Over-cite Count': 13}, 'Paper Title: Directional routing and scheduling for green vehicular delay tolerant networks'],


[{'Citing Paper Number': 1, 'Over-cite Count': 3}, {'Citing Paper Number': 2, 'Over-cite Count': 2}, {'Citing Paper Number': 3, 'Over-cite Count': 1}, {'Citing Paper Number': 4, 'Over-cite Count': 1}, {'Citing Paper Number': 6, 'Over-cite Count': 1}, {'Citing Paper Number': 7, 'Over-cite Count': 1}, 'Paper Title: Routing for disruption tolerant networks: taxonomy and design'],

[{'Over-cite Count': 2, 'Citing Paper Number': 1}, {'Over-cite Count': 1, 'Citing Paper Number': 3}, {'Over-cite Count': 1, 'Citing Paper Number': 4}, {'Over-cite Count': 3, 'Citing Paper Number': 5}, {'Over-cite Count': 1, 'Citing Paper Number': 6}, 'Paper Title: Molecular communication and networking: Opportunities and challenges'],
[{'Citing Paper Number': 1, 'Over-cite Count': 0}, {'Citing Paper Number': 2, 'Over-cite Count': 1}, {'Citing Paper Number': 3, 'Over-cite Count': 1}, {'Citing Paper Number': 4, 'Over-cite Count': 0}, {'Citing Paper Number': 5, 'Over-cite Count': 13}, 'Paper Title: Routing metrics of cognitive radio networks: A survey'],

[{'Citing Paper Number': 1, 'Over-cite Count': 3}, {'Citing Paper Number': 2, 'Over-cite Count': 1}, {'Citing Paper Number': 3, 'Over-cite Count': 0}, {'Citing Paper Number': 4, 'Over-cite Count': 1}, {'Citing Paper Number': 5, 'Over-cite Count': 2}, {'Citing Paper Number': 6, 'Over-cite Count': 2}, {'Citing Paper Number': 7, 'Over-cite Count': 1}, {'Citing Paper Number': 8, 'Over-cite Count': 3}, {'Citing Paper Number': 9, 'Over-cite Count': 2}, 'Paper Title: An adaptive geometry-based stochastic model for non-isotropic MIMO mobile-to-mobile channels'],

[{'Citing Paper Number': 1, 'Over-cite Count': 13}, {'Citing Paper Number': 2, 'Over-cite Count': 0}, {'Citing Paper Number': 3, 'Over-cite Count': 8}, 'Paper Title: EDAL: An energy-efficient, delay-aware, and lifetime-balancing data collection protocol for heterogeneous wireless sensor networks'],

[{'Citing Paper Number': 1, 'Over-cite Count': 5}, {'Citing Paper Number': 2, 'Over-cite Count': 9}, {'Citing Paper Number': 3, 'Over-cite Count': 7}, {'Citing Paper Number': 4, 'Over-cite Count': 13}, {'Citing Paper Number': 5, 'Over-cite Count': 0}, 'Paper Title: A survey on topology control in wireless sensor networks: Taxonomy, comparative study, and open issues'],

[{'Citing Paper Number': 2, 'Over-cite Count': 9}, {'Citing Paper Number': 4, 'Over-cite Count': 0}, {'Citing Paper Number': 5, 'Over-cite Count': 1}, {'Citing Paper Number': 6, 'Over-cite Count': 0}, {'Citing Paper Number': 7, 'Over-cite Count': 1}, 'Paper Title: A survey on the ietf protocol suite for the internet of things: Standards, challenges, and opportunities']]

writer = csv.writer(open('over_cites.csv', 'w'), lineterminator='\n')
for paper in over_cite_arr:
    
    writer.writerow([paper[-1]])
    arr_len = len(paper)
    headers =['Citing Paper Number', 'Over-cite Count']
    writer.writerow(headers)
    paper.pop()
    total =0
    for dict_item in paper:
        writer.writerow([dict_item['Citing Paper Number'], dict_item['Over-cite Count']])
        total+=dict_item['Over-cite Count']
    writer.writerow(['Total', total])
    writer.writerow(['\n'])
'''
    

