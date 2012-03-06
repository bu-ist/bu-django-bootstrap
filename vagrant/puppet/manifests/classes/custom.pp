# Files and settings specific to the app

class custom {
    file {
        "/etc/apache2/sites-available/djangoapp":
            content => template("djangoapp.conf.erb"),
            ensure => file,
            require => Package["apache2-mpm-worker"];
        "/etc/apache2/sites-enabled/001-djangoapp":
            ensure => "/etc/apache2/sites-available/djangoapp",
            require => Package["apache2-mpm-worker"];
        "/etc/apache2/sites-enabled/000-default":
            ensure => absent,
            require => Package["apache2-mpm-worker"];
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
        "/var/apps/djangoapp/releases/current":
            owner => 'vagrant',
            group => 'www-data',
            ensure => link,
            target => '/app';
    }
    
    # initialize app
    exec { '/usr/local/bin/fab vagrant setup_vagrant':
        cwd => '/var/apps/djangoapp/releases/current',
        user => 'vagrant',
        group => 'www-data',
        logoutput => true,
        # this might take a while, since it's installing packages - disable timeout
        timeout => 0
    }
    
    # startup dir
    append_if_no_such_line {
        startup_dir:
            file => "/home/vagrant/.profile",
            line => "if [ -e /var/apps/djangoapp/releases/current ]; then cd /var/apps/djangoapp/releases/current; fi;";
    }
    

}
