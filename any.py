#!/usr/bin/python
from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.compute.types import Provider as ComputeProvider
from libcloud.compute.base import NodeAuthSSHKey
from libcloud.compute.base import NodeImage, NodeSize, NodeLocation
from libcloud.compute.types import NodeState
from libcloud.compute.base import Node, NodeDriver

import time

VR = get_compute_driver(ComputeProvider.HOSTVIRTUAL)

#driver = VR('AuIiy4nZrk2o5ZdNbpwsUunCcZnevaxH^nEqD2E0x1Bc5OvBmm.A5A.F4t66mdSVumGCbfFhUC'); # group1-1
#driver = VR('TmpAUYxVjNXitc4pmXSl8n2ym73iBmiw-wejgqhDgTS^doAvhzNqXu7wh0m9GEQ4bn0NigIYFW'); # balancer
#driver = VR('7aoFCouBzIUAMCFU5Wf0a0UoObhXcATXlNrY^ZjK5v9Epllpi2nf0VHeqWDQhhwjKxxHyvA^al'); #adjust
#driver = VR('mGfeHdkimn3thGuNH94GNgvb0qbpRj3vAkzpMqZmNrayvz1HqdGWVMtFRxVEyw8KCbR5x6tNxU'); #turboflix
#driver = VR('wF2LYpV.-KXOegYSTSaTj3nPi4ZxYvnW^1KJTI^8m0AUxpJx20AuG6k5jqiE3cPuUqmuMmX6he'); #cedexis
#driver = VR('9yZuz.aWub05sW0SP1v71S6-H41.10Bc9qASCpS.GM8TuusQuGYHocmZdUGuAb-seMwZpuFwNM'); #mcafee
#driver = VR('b3yujsRfNfLmNkdFJL-D2FQH-yJO8VkTQfbP6vfFqe3vluSGstQfiwbNOqu9yMMgT-H2.xFzpH'); #netlify
#driver = VR('JbVBD29FGMSw5B.mezqQ-TSulrvl0WSXeRUm9TF20k9HZlaPNGi6-NAvb6epX404n9CfLPKntV'); #zycada
# driver = VR('0gnNtklGYqv059TMKAa02zVmn4NczvtPLala11xzui^iWZqdB0Dp3Zn-qmFasOEZSre0OmWaio'); #nsone
driver = VR('7yYjNWbT.aK5BWhZr0d4-DcxlkkHYt046Kb^KkDeakYMP7r4rlR9lWrCbHu-^0BJZiAb^RuAf^') # bill duggin

#api_key = raw_input("Please enter CX API key:")
#if api_key:
    #driver = VR(api_key)

#ssh_key_string = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA06ifR1Movjcmyql1Fb8rNzJl7my9E1bYU2xq8Dfgx42f0I//s9U9WeUX4fxQPFPzN0jvfN5Dx51tMR2rvI5ruVH6mlkkRmn3mSPW536BRBWBPyLcVHOaWmGBebiMyEQFAYwJ4ToJQ5i+rQA/IDL8hOeDFxu4Pi6Kgp/l7hAAeTgfkPdPO3BEB5nxV8BFXZAq4zjlrX+WFv5iiIrxkGV1aJcGzf1YOq6uI1s2IoT1mdqcPlx8DlvxMk6tG3bOVJqfhP2MDE+amKPZUF3s0A7uxgdO2WJ0hO7Ynpf9xxh4vU4JB9JkzjcxWf4GPUdMTYRVPGBUBOg+Mkc0i6YichTdkQ== cedexis_user@dev'
ssh_key_string = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/wEh+AG/MfGcBHiJM1r8avg/RzXKYvxypiNqFa+5Vuhwm+ea8fNIKW3SeERrCy47Bx/l1ViRtOCZuonfN1qmVXh46b+GItgxrTuqYMsenEMNeyCRFIk1NdR1XYUYwkKQtj+etwaXPluDGwKcpfFINo6Gz2uL2/wIMqzD3kKOyKBay9wZYW6OgDtwjn9h8/LX82BItOgRIxDV+8NIlJLyMXbAq0soa8BN9+P6H2C8/bc/CzA7oGkQt3RWVtmJ+PrjzJFKo8iR8J8PQ7Uf4jkacQnKvboeXKUIeCRs3JkIv732lBAfxWOsyHOe064se1EYpyVCagBkfZEODvCZ65PkL d@carbon-bitch'

locations = driver.list_locations()

loc_map = { #vyatta map
    'svm': 'bl',
    'lax': 'lax3',
    'sjc': 'sjc',
    'iad': 'iad2',
    'lga': 'ny',
    'ord': 'chi',
    'sea': 'sea',
    'dfw': 'dfw',
    'mia': 'mia',
    'den': 'den',
    'yyz': 'tor',
    'lhr': 'uk',
    'fra': 'de', #frankfurt
    'ams': 'nl',
    'cdg': 'fr', #france
    'otp': 'otp',
    'hkg': 'hk',
    'maa': 'maa',
    'sin': 'sg',
    'syd': 'syd',
    'gru': 'gru',
}

nodes = driver.list_nodes()

def generate_deploy(hostname, domain):
    pkgs = driver.ex_list_packages()
    for p in pkgs:
        for l in locations:
            if l.name == p.extra['city']:
                loc = l.name.split(' ')[0]
            else:
                loc = 'xxx'
        #print hostname+'-'+loc.lower()+'.'+domain+'|'+p.id+'|'+p.extra['package']+'|'
        if p.extra['installed'] is None:
            print hostname+'-'+loc.lower()+'.'+domain+'|'+p.id+'|'+p.extra['package']+'|'

def generate_inventory(host_filter=''):
    for node in nodes:
        if node.state == NodeState.RUNNING:
            loc = ''
            for l in locations:
                if l.id == node.extra['location']:
                    loc = l.name.split(' ')[0]
                    loc = loc.lower()
            if host_filter in node.name:
                print node.name+" "+"ansible_ssh_host="+node.public_ips[0]
                #print node.name+" eth0_v6="+node.extra['data']['ipv6']
                #print node.name+" eth0_v6="+node.extra['data']['ipv6']

def generate_sessions(host_filter=''):
    for node in nodes:
        if node.state == NodeState.RUNNING:
            loc = ''
            for l in locations:
                if l.id == node.extra['location']:
                    loc = l.name.split(' ')[0]
                    loc = loc.lower()
            if host_filter in node.name:
                if loc in loc_map:
                    print 'vyatta-'+loc_map[loc]+':'+node.public_ips[0]
                else:
                    print 'vyatta-'+loc+':'+node.public_ips[0]

def generate_sessions6(host_filter=''):
    for node in nodes:
        if node.state == NodeState.RUNNING:
            loc = ''
            for l in locations:
                if l.id == node.extra['location']:
                    loc = l.name.split(' ')[0]
                    loc = loc.lower()
            if host_filter in node.name:
                if loc in loc_map:
                    print 'vyatta-'+loc_map[loc]+'#'+node.extra['data']['ipv6']
                else:
                    print 'vyatta-'+loc+'#'+node.extra['data']['ipv6']


def deploy_nodes(nodefile):
    #size = [s for s in sizes if s.ram == '1024MB'][0]
    #loc = [l for l in locations if l.id == '21'][0]
    #image = [i for i in images if i.id == '4538'][0]
    loc = {'id': 21}
#    image = NodeImage(id='4664',name="blah",driver=driver)
    image = NodeImage(id='4592', name="blah", driver=driver)

    #node = [n for n in pkgs if n.id == '152624'][0]

    f = open(nodefile, 'r')
    for l in f:
        l = l.rstrip().split('|')
        force=l[3]
        name = l[0]
        id = l[1]
        public_ips = []
        private_ips = []
        extra = {}

        state = NodeState.STOPPED
        node = Node(id=id, name=name, state=state,
                    public_ips=public_ips, private_ips=private_ips,
                    driver=driver, extra=extra)
        node.extra['location'] = loc['id']
        print node.__dict__
        n = driver.ex_provision_node(image=image,
                                     auth=NodeAuthSSHKey(ssh_key_string),
                                     force=force, node=node)
        print n
        #n = driver.ex_start_node(node=node)
        #n = driver.ex_delete_node(node=node)
        time.sleep(3)

#generate_deploy('anycast','netlify.priv')
#generate_sessions()
#generate_sessions6()
generate_inventory(host_filter='den')
#deploy_nodes('b.txt')
