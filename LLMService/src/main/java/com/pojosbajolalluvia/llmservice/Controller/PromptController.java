package com.pojosbajolalluvia.llmservice.Controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/prompt")
public class PromptController {
    @GetMapping
    public String getRespuesta(String mensaje){
        return "respuesta";
    }
}
