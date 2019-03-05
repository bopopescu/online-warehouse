import { Component, OnInit } from '@angular/core';
import { NavService } from '../../services/nav.service';
import { ValidateService } from '../../services/validate.service';
import {Router} from '@angular/router';
import {FlashMessagesService} from 'angular2-flash-messages';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  email:String;
  password:String;

  constructor(
    public nav: NavService,
    public validateService: ValidateService,
    public router: Router,
    public flashMessage: FlashMessagesService
  ) { }

  ngOnInit() {
    this.nav.hide();
  }

  onLoginSubmit(){
  const user = {
    email: this.email,
    password: this.password
  }
  console.log(user);

  if(!this.validateService.validateLogin(user)){
    this.flashMessage.show('Please fill in all fields', {cssClass: 'alert-danger', timeout: 3000});
    return false;
  }

  // this.authService.authenticateUser(user).subscribe(data => {
  //   if(data.success){
  //     this.authService.storeUserData(data.token, data.user);
  //     this.flashMessage.show("Logged in!",{
  //       cssClass: 'alert-success',
  //       timeout: 5000})
  //       this.router.navigate(['/dashboard']);
  //
  //   } else{
  //     this.flashMessage.show(data.msg,{
  //       cssClass: 'alert-danger',
  //       timeout: 5000
  //     })
  //     this.router.navigate(['/login']);
  //   }
  //
  // })
}

}