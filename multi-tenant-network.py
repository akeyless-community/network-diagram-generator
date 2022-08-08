from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.compute import ComputeEngine
from diagrams.gcp.database import SQL
from diagrams.gcp.network import TrafficDirector, NAT, DNS
from diagrams.aws.network import Route53, NLB
from diagrams.azure.compute import VM
from diagrams.azure.database import SQLDatabases
from diagrams.azure.network import RouteFilters, LoadBalancers as AzLB
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Traefik
from diagrams.generic.network import Firewall
from diagrams.k8s.compute import Deploy
from diagrams.k8s.group import NS
from diagrams.k8s.network import Ingress

with Diagram("Multi-Tenant Network Diagram", show=True, direction="BT"):
    with Cluster("Akeyless Cloud Platform", direction="LR"):
        # dns = Route53("vault.akeyless.io:443\napi.akeyless.io:443\nrest.akeyless.io:443\nconsole.akeyless.io:443\nauth.akeyless.io:443\naudit.akeyless.io:443\nbis.akeyless.io:443\ngator.akeyless.io:443\nkfm[1-4].akeyless.io:443\nakeyless-cli.s3.us-east-2.amazonaws.com:443\nakeylessservices.s3.us-east-2.amazonaws.com:443\nsqs.us-east-2.amazonaws.com:443\ntcp://log.akeyless.io:9997\ntcp://log.akeyless.io:9443\namqps://mq.akeyless.io:5671")
        dns = DNS("DNS")
        glb = NLB("Global Network Load Balancer\n(Latency-Based Routing)")
        with Cluster("Cloud Services Provider 2"):
            csp2Lb = LoadBalancing("Cloud Service Provider 1")
            with Cluster("CSP2 VPC A"):
                with Cluster("Region A"):
                    with Cluster("Availability Zone 1"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rule"):
                                csp2_sql1 = SQL("SQL")
                            with Cluster("Instance Group"):
                                csp2_gce1 = [ComputeEngine("Server"),
                                ComputeEngine("Server")]
                    with Cluster("Availability Zone 2"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rule"):
                                csp2_sql2 = SQL("SQL")
                            with Cluster("Instance Group"):
                                csp2_gce2 = [ComputeEngine("Server"),
                                ComputeEngine("Server")]
                    with Cluster("Public Subnet"):
                        csp2_rtr1 = TrafficDirector("")
            with Cluster("CSP1 VPC B"):
                with Cluster("Region B"):
                    with Cluster("Availability Zone 1"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rules"):
                                csp2_sql3 = SQL("SQL")
                            with Cluster("Instance Group"):
                                csp2_gce3 = [ComputeEngine("Server"),
                                ComputeEngine("Server")]
                    with Cluster("Availability Zone 2"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rule"):
                                csp2_sql4 = SQL("SQL")
                            with Cluster("Instance Group"):
                                csp2_gce4 = [ComputeEngine("Server"),
                                ComputeEngine("Server")]
                    with Cluster("Public Subnet"):
                        csp2_rtr2 = TrafficDirector("")
        with Cluster("Cloud Services Provider 1"):
            csp1Lb = AzLB("Cloud Service Provider 1")
            with Cluster("CSP1 VPC A"):
                with Cluster("Region A"):
                    with Cluster("Availability Zone 1"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rule"):
                                csp1_sql1 = SQLDatabases("SQL")
                            with Cluster("Instance Group"):
                                csp1_gce1 = [VM("Server"),
                                VM("Server")]
                    with Cluster("Availability Zone 2"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rule"):
                                csp1_sql2 = SQLDatabases("SQL")
                            with Cluster("Instance Group"):
                                csp1_gce2 = [VM("Server"),
                                VM("Server")]
                    with Cluster("Public Subnet"):
                        csp1_rtr1 = RouteFilters("")
            with Cluster("CSP1 VPC B"):
                with Cluster("Region B"):
                    with Cluster("Availability Zone 1"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rules"):
                                csp1_sql3 = SQLDatabases("SQL")
                            with Cluster("Instance Group"):
                                csp1_gce3 = [VM("Server"),
                                VM("Server")]
                    with Cluster("Availability Zone 2"):
                        with Cluster("Private Subnet"):
                            with Cluster("Firewall Rule"):
                                csp1_sql4 = SQLDatabases("SQL")
                            with Cluster("Instance Group"):
                                csp1_gce4 = [VM("Server"),
                                VM("Server")]
                    with Cluster("Public Subnet"):
                        csp1_rtr2 = RouteFilters("")
    with Cluster("Customer Network", direction="LR"):
        fw1 = Firewall("Customer Firewall")
        with Cluster("Data Center 1"):
            onPremNat = NAT("On-Premise NAT")
            onPremLb = LoadBalancing("On-Premise Load Balancer")
            with Cluster("Region A"):
                with Cluster("Availability Zone 1"):
                    with Cluster("VM Host"):
                        agw1 = Docker("Akeyless Gateway Cluster 1")
                    with Cluster("Customer App Host 5"):
                        app5 = Server("Customer App 5")
                with Cluster("Availability Zone 2"):
                    with Cluster("VM Host"):
                        agw2 = Docker("Akeyless Gateway Cluster 1")
                    with Cluster("Customer App Host 3"):
                        app3 = Server("Customer App 3")
                with Cluster("Kubernetes Cluster"):
                    with Cluster("Akeyless Namespace"):
                        agw2_deploy1 = Deploy("Akeyless Gateway\nCluster 2")
                        ingr3 = Ingress("Akeyless Gateway\nIngress")
                    with Cluster("Customer App 4 Namespace"):
                        inject2 = Deploy("Akeyless Secrets\nInjector")
                        app4 = Deploy("Customer App 4")
            with Cluster("Region B"):
                with Cluster("Availability Zone 1"):
                    with Cluster("VM Host"):
                        agw3 = Docker("Akeyless Gateway")
                    with Cluster("Customer App Host 1"):
                        app1 = Server("Customer App 1")
                with Cluster("Availability Zone 2"):
                    with Cluster("VM Host"):
                        agw4 = Docker("Akeyless Gateway")
                    with Cluster("Customer App Host 2"):
                        app2 = Server("Customer App 2")
        with Cluster("Cloud Service Provider 1"):
            nat = NAT("Cloud Service Provider 1 NAT")
            with Cluster("Region A"):
                with Cluster("Availability Zone 1"):
                    with Cluster("Kubernetes Cluster"):
                        with Cluster("Akeyless Namespace"):
                            agw3_deploy1 = Deploy("Akeyless Gateway Cluster 3")
                            ingr1 = Ingress("Akeyless Gateway\nIngress")
                        with Cluster("Customer App1 Namespace"):
                            inject1 = Deploy("Akeyless Secrets\nInjector")
                            csp1_deploy1 = Deploy("Customer App1")
                    with Cluster("VM Host"):
                        csp1_vm1 = [ComputeEngine("Server"),
                        ComputeEngine("Server")]
                with Cluster("Availability Zone 2"):
                    with Cluster("Kubernetes Cluster"):
                        with Cluster("Akeyless Namespace", direction="TB"):
                            agw3_deploy2 = Deploy("Akeyless Gateway\nCluster 4")
                            ingr2 = Ingress("Akeyless Gateway\nIngress")
                    with Cluster("VM Host"):
                        csp1_vm2 = [ComputeEngine("Server"),
                        ComputeEngine("Server")]
            with Cluster("Region B"):
                with Cluster("Availability Zone 1"):
                    with Cluster("VM Host"):
                        csp1_vm3 = [ComputeEngine("Server"),
                        ComputeEngine("Server")]
                with Cluster("Availability Zone 2"):
                    with Cluster("VM Host"):
                        agw5 = Docker("Akeyless Gateway")
                    csp1_vm4 = [ComputeEngine("Server"),
                        ComputeEngine("Server")]

    # DNS to GLB
    dns >> glb
    
    # GLB to CSPs
    glb >> [csp1Lb, csp2Lb]
    ## Cloud Service Provider 1
    csp1Lb >> [csp1_rtr1, csp1_rtr2]
    csp1_rtr1 >> csp1_gce1
    csp1_rtr1 >> csp1_gce2

    csp1_gce1 >> csp1_sql1
    csp1_gce2 >> csp1_sql2

    csp1_rtr2 >> csp1_gce3
    csp1_rtr2 >> csp1_gce4

    csp1_gce3 >> csp1_sql3
    csp1_gce4 >> csp1_sql4

    ## Cloud Service Provider 2
    csp2Lb >> [csp2_rtr1, csp2_rtr2]
    csp2_rtr1 >> csp2_gce1
    csp2_rtr1 >> csp2_gce2

    csp2_gce1 >> csp2_sql1
    csp2_gce2 >> csp2_sql2

    csp2_rtr2 >> csp2_gce3
    csp2_rtr2 >> csp2_gce4

    csp2_gce3 >> csp2_sql3
    csp2_gce4 >> csp2_sql4

    ## Customer to AVP
    [agw1, agw2, agw3, agw4, agw2_deploy1 ] >> onPremNat >> Edge(label="Traffic to Akeyless Vault Platform (443)", style="line") >> dns

    [agw3_deploy1, agw3_deploy2, agw5] >> nat >> Edge(label="Traffic to Akeyless Vault Platform (443)", style="line") >> dns
    ## Customer CSP to GW
    csp1_deploy1 >> inject1
    csp1_vm1 >> ingr1
    csp1_vm2 >> ingr2
    csp1_vm3 >> agw5
    csp1_vm4 >> agw5
    inject1 >> ingr1
    ingr2 >> agw3_deploy2
    ingr3 >> agw2_deploy1
    ingr1 >> agw3_deploy1

    ## Customer On-Prem to GW
    app1 >> onPremLb
    app2 >> onPremLb
    app3 >> onPremLb
    app4 >> inject2 >> ingr3
    app5 >> onPremLb
    onPremLb >> [agw1, agw2, agw3, agw4]