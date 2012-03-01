# Basic startup stuff

class init {
    # Users/groups
    group {
        "puppet":
            ensure => "present";
    }
    
    # apt-get update to update package lists
    exec { "apt-get update":
        command => '/usr/bin/apt-get update'
    }
    
    # sudoers, .profile
    append_if_no_such_line {
        sudoers:
            file => "/etc/sudoers",
            line => "%admin ALL=(ALL) ALL";
            
        virtualenv:
            file => "/home/vagrant/.profile",
            line => "if [ -e /var/apps/djangoapp/venv/bin/activate ]; then source /var/apps/djangoapp/venv/bin/activate; fi;";
    }
}
