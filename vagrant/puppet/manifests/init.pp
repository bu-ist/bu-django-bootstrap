# Basic startup stuff

class init {

    # Users/groups
    group {
        "puppet":  ensure => "present";
    }
    
    # apt-get update to update package lists
    exec { "apt-get update":
    	command => '/usr/bin/apt-get update';
	}

    file {
        "/var/apps":
            ensure => directory;
        "/var/apps/djangoapp":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/var/apps/djangoapp/htdocs":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/var/apps/djangoapp/htdocs/uploads":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/var/apps/djangoapp/log":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/var/apps/djangoapp/app":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/var/apps/djangoapp/venv":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/var/apps/djangoapp/releases":
            owner => 'vagrant',
            group => 'www-data',
            ensure => directory;
        "/app/repo":
            ensure => directory;
        "/var/apps/djangoapp/releases/current":
            owner => 'vagrant',
            group => 'www-data',
            ensure => link,
            target => "/app/repo";
    } 
}
