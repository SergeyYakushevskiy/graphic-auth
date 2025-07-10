package dstu.csae.auth.graphic.security;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;

@Component
public class JwtCore {
    @Value("${app.secret}")
    private String secret;
    @Value("${app.secret.expirationMs}")
    @Getter
    private int lifetime;

    private Key getSigningKey() {
        byte[] keyBytes = secret.getBytes(StandardCharsets.UTF_8);
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            keyBytes = digest.digest(keyBytes);
        }catch (NoSuchAlgorithmException ex){
            ex.printStackTrace();
        }
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public String generateToken(Authentication authentication){
        AccountDetailsImpl userDetails = (AccountDetailsImpl) authentication.getPrincipal();
        return Jwts.builder()
                .setSubject(userDetails.getIdentifier())
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + lifetime))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public String getNameFromJwt(String token){
        return Jwts.parser()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

}
