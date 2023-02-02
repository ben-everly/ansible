# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  config.vm.provision "ansible_local" do |ansible|
    ansible.galaxy_role_file = "roles/requirements.yml"
    ansible.galaxy_roles_path = "/home/vagrant/.ansible/roles"
    ansible.inventory_path = "/vagrant/inventory"
    ansible.limit = "workstation"
    ansible.playbook = "playbook.yml"
  end
end
