# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "personal" do |personal|
    personal.vm.box = "ubuntu/jammy64"
    personal.vm.hostname = "test"
    personal.vm.provision "ansible_local" do |ansible|
      ansible.galaxy_role_file = "roles/requirements.yml"
      ansible.galaxy_roles_path = "/home/vagrant/.ansible/roles"
      ansible.inventory_path = "/vagrant/inventory"
      ansible.limit = "workstation"
      ansible.playbook = "playbook.yml"
    end
  end

  config.vm.define "work" do |work|
    work.vm.box = "ubuntu/jammy64"
    work.vm.hostname = "work"
    work.vm.provision "ansible_local" do |ansible|
      ansible.galaxy_role_file = "roles/requirements.yml"
      ansible.galaxy_roles_path = "/home/vagrant/.ansible/roles"
      ansible.inventory_path = "/vagrant/inventory"
      ansible.limit = "workstation"
      ansible.playbook = "playbook.yml"
    end
  end

  config.vm.define "server" do |server|
    server.vm.box = "debian/bullseye64"
    server.vm.network "private_network", ip: "192.168.56.2"
    server.vm.provision "ansible" do |ansible|
      ansible.galaxy_role_file = "./roles/requirements.yml"
      ansible.galaxy_roles_path = "/$HOME/.ansible/roles"
      ansible.limit = "server"
      ansible.playbook = "playbook.yml"
    end
  end

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end
end
