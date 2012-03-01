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
        ensure => "1.4.8",
        require => Package["python-pip"],
        provider => pip;
    }
    package { "fabric":
        ensure => "1.3.3",
        require => Package["python-pip"],
        provider => pip;
    }
    package { "virtualenvwrapper":
        ensure => "3.0.1",
        require => Package["python-pip"],
        provider => pip;
    }
}
