# Apache/WSGI

class apache {
    package {
        "apache2-mpm-worker":
            ensure => "2.2.14-5ubuntu8.8";
        "libapache2-mod-wsgi":
            ensure => "2.8-2ubuntu1";
    }

    service { "apache2":
        enable => true,
        ensure => running,
        require => Package["apache2-mpm-worker"],
    }
}
