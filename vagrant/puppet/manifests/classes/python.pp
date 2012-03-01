# Python
class python {
    package {
        "build-essential": ensure => latest;
        "python": ensure => "2.6.5-0ubuntu1";
        "python-dev": ensure => "2.6.5-0ubuntu1";
        "python-setuptools": ensure => "latest";
        "python-pip": ensure => "latest";
    }
    
    # Virtualenv, Fabric
    package { "virtualenv":
        ensure => "1.7.1.2",
        require => Package["python-pip"],
        provider => pip;
    }
    package { "fabric":
        ensure => "1.4.0",
        require => Package["python-pip"],
        provider => pip;
    }
}
