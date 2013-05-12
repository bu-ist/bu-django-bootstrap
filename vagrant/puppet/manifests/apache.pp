# Apache/WSGI

class apache {
    package {
        "apache2-mpm-worker":
            ensure => installed;
        "libapache2-mod-wsgi":
            ensure => installed;
    }
 
    service { "apache2":
        enable => true,
        ensure => running,
        require => Package["apache2-mpm-worker"],
    }

    file{
        "/etc/apache2/sites-available/djangoapp":
            content => template("/app/vagrant/puppet/templates/vhost.erb"),
            ensure => file,
            require => Package["apache2-mpm-worker"];
        "/etc/apache2/sites-enabled/001-djangoapp":
            ensure => "/etc/apache2/sites-available/djangoapp",
            require => Package["apache2-mpm-worker"];
        "/etc/apache2/sites-enabled/000-default":
            ensure => absent,
            require => Package["apache2-mpm-worker"];
    }
}
