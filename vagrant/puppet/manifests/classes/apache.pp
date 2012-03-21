# Apache/WSGI

class apache {
    package {
        "apache2-mpm-worker":
            ensure => present;
        "libapache2-mod-wsgi":
            ensure => present;
    }

    service { "apache2":
        enable => true,
        ensure => running,
        require => Package["apache2-mpm-worker"],
    }
}
