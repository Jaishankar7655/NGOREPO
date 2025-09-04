resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file("my-keys.pub")

}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "default-vpc"
  }
}

resource "aws_security_group" "my_sg" {
  name        = "my-security-group"
  description = "Allow SSH and HTTP"
  vpc_id      = aws_default_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }


  tags = {
    Name = "my-security-group"
  }
}

resource "aws_instance" "myweb" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name        = aws_key_pair.deployer.key_name
 vpc_security_group_ids = [aws_security_group.my_sg.id]
  tags = {
    Name = var.instance_name
  }

  root_block_device {
  volume_size           = var.root_volume_size
    volume_type           = var.root_volume_type
    delete_on_termination = true
  }



}
